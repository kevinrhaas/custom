# Local face matching dependencies

Pinned source: https://github.com/justadudewhohacks/face-api.js/tree/0.22.2

`face-api.min.js` is face-api.js 0.22.2, including TensorFlow.js core 1.7.0 and tslib helpers. It is served from this directory; no runtime CDN is used. Only tiny face detection, tiny 68-point landmarks and face recognition models are loaded. No age, gender or emotion models are included.

Licenses: face-api.js and its distributed model files: MIT (`LICENSE`); bundled TensorFlow.js: Apache 2.0 (`LICENSE.tensorflow`); tslib: Apache 2.0 and Microsoft copyright notice. Model and library source URLs use the pinned 0.22.2 tag. Dependency license files come from their upstream repositories/package distributions.

The admin tool downloads about 7.4 MB of code and weights, on demand. Selected images, crops and descriptors stay in memory in the browser. They are discarded when the tool is cleared or the page is closed. Only names explicitly added to review can be exported.

## SHA-256

```text
19246466cb51e46c12b22e43b4d2703ac981cb4295d061d6e20609bd5845510b  CopyrightNotice.tslib.txt
d5480b4d4e46880107a56db666697ec3e90def81a8fc829e530b1c291e3172a5  LICENSE
cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30  LICENSE.tensorflow
a7d00bfd54525bc694b6e32f64c7ebcf5e6b7ae3657be5cc12767bce74654a47  LICENSE.tslib.txt
5d66ec95338d7fcc365ce15481b8599baf4b6e22c9a624b76d4ca821a669a659  face-api.min.js
b98e9f2f7da76f8a6dda9741a36ed485b224b889d552de2b2c1bb16217f67bfc  models/face_landmark_68_tiny_model-shard1
3c63b8984302c187b218d9ef5aa149ed8c2c7fa3fe54db078614692bc48d153c  models/face_landmark_68_tiny_model-weights_manifest.json
412566a2b8d814d84c60b8055ec5d3b3b2328ef7cd7853384e03ec3db7b053d8  models/face_recognition_model-shard1
69350fdecd845c532e44dd8f7d0521c773505ef46b87cc34f46640a0cc334ecc  models/face_recognition_model-shard2
6619f4126f845c1f7857f39cbd79565f375734f46e0dd25d9602f8dc21cda9f5  models/face_recognition_model-weights_manifest.json
b7503ce7df31039b1c43316a9b865cab6a70dd748cc602d3fa28b551503c3871  models/tiny_face_detector_model-shard1
14c60659a31b6b7b1320077171b8f8adcb24ef0e62dde62ce603bcb49a1b49b5  models/tiny_face_detector_model-weights_manifest.json
```
