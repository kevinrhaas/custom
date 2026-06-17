include <awning.scad>
union(){
  render() intersection(){ straight_raw(corner_leg,0); keep_ZX(); }
  render() mirror([1,0,-1]) intersection(){ straight_raw(corner_leg,0); keep_ZX(); }
}
