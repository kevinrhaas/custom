// The model and every weight are served by this site. Images are decoded and
// examined locally; nothing from a selected file is sent over the network.
let modelPromise;
const vendorRoot = new URL('../vendor/face-api/', import.meta.url);

export function descriptorDistance(a, b) {
  if (!a?.length || a.length !== b?.length) return Infinity;
  let sum = 0;
  for (let i = 0; i < a.length; i++) {
    if (!Number.isFinite(a[i]) || !Number.isFinite(b[i])) return Infinity;
    sum += (a[i] - b[i]) ** 2;
  }
  return Math.sqrt(sum);
}

// Complete-link groups avoid chaining a weak match through a third face.
// Two faces in the same photo can never be grouped together automatically.
export function groupFaces(faces, threshold = 0.5) {
  const groups = [];
  for (const face of faces) {
    let best = null, bestDistance = Infinity;
    for (const group of groups) {
      if (group.some(other => other.photoId === face.photoId)) continue;
      const distance = Math.max(...group.map(other => descriptorDistance(face.descriptor, other.descriptor)));
      if (distance <= threshold && distance < bestDistance) {
        best = group; bestDistance = distance;
      }
    }
    if (best) best.push(face);
    else groups.push([face]);
  }
  return groups.sort((a, b) => b.length - a.length);
}

export function collectPeople(groups) {
  const result = Object.create(null);
  for (const group of groups) {
    for (const face of group.faces) {
      if (face.excluded) continue;
      const name = (face.name || group.name || '').trim();
      if (!name) continue;
      const people = (result[face.photoId] ||= { people: [] }).people;
      if (!people.some(existing => existing.toLocaleLowerCase() === name.toLocaleLowerCase())) people.push(name);
    }
  }
  return result;
}

export async function loadFaceModels() {
  if (!modelPromise) modelPromise = (async () => {
    if (!window.faceapi) await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = new URL('face-api.min.js', vendorRoot).href;
      script.onload = resolve;
      script.onerror = () => { script.remove(); reject(new Error('The face tools could not load. Check your connection and try again.')); };
      document.head.append(script);
    });
    const api = window.faceapi;
    // Use the device's GPU when available, with a CPU fallback for older phones.
    try { if (!await api.tf.setBackend('webgl')) await api.tf.setBackend('cpu'); }
    catch { await api.tf.setBackend('cpu'); }
    const models = new URL('models/', vendorRoot).href;
    await Promise.all([
      api.nets.tinyFaceDetector.loadFromUri(models),
      api.nets.faceLandmark68TinyNet.loadFromUri(models),
      api.nets.faceRecognitionNet.loadFromUri(models),
    ]);
    return api;
  })().catch(error => { modelPromise = null; throw error; });
  return modelPromise;
}

export async function inspectLocalPhoto(file, photoId) {
  if (file.size > 30 * 1024 * 1024) throw new Error('This file is over 30 MB. Choose a smaller JPG or PNG copy.');
  const api = await loadFaceModels();
  const url = URL.createObjectURL(file);
  const img = new Image();
  try {
    img.src = url;
    await img.decode();
    if (!img.naturalWidth || !img.naturalHeight) throw new Error('The image is empty.');
    const scale = Math.min(1, 1600 / Math.max(img.naturalWidth, img.naturalHeight));
    const canvas = document.createElement('canvas');
    canvas.width = Math.max(1, Math.round(img.naturalWidth * scale));
    canvas.height = Math.max(1, Math.round(img.naturalHeight * scale));
    canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
    const detections = await api.detectAllFaces(canvas, new api.TinyFaceDetectorOptions({inputSize: 416, scoreThreshold: 0.35}))
      .withFaceLandmarks(true).withFaceDescriptors();
    const faces = detections.map((result, index) => {
      const box = result.detection.box;
      const padding = Math.max(box.width, box.height) * 0.2;
      const x = Math.max(0, box.x - padding), y = Math.max(0, box.y - padding);
      const width = Math.min(canvas.width - x, box.width + padding * 2);
      const height = Math.min(canvas.height - y, box.height + padding * 2);
      const crop = document.createElement('canvas');
      crop.width = 144; crop.height = 144;
      const context = crop.getContext('2d');
      context.fillStyle = '#ddd'; context.fillRect(0, 0, 144, 144);
      const fit = Math.min(144 / width, 144 / height);
      context.drawImage(canvas, x, y, width, height, (144 - width * fit) / 2, (144 - height * fit) / 2, width * fit, height * fit);
      return { id: `${photoId}:${index}`, photoId, descriptor: Array.from(result.descriptor), thumbnail: crop.toDataURL('image/jpeg', 0.85) };
    });
    canvas.width = canvas.height = 0;
    return faces;
  } catch (error) {
    if (error.name === 'EncodingError') throw new Error('This image could not be opened. Choose a JPG, PNG or WebP copy.');
    throw error;
  } finally {
    URL.revokeObjectURL(url);
    img.src = '';
  }
}
