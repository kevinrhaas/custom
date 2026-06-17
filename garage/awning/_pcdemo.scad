// endcap + a green SIDE PLEXI sheet seated in the groove (to verify capture)
color([0.85,0.7,0.1]) import("part_plexicap.stl");
// derived (mirror of awning.scad defaults)
oh_under=2; side_fascia_drop=18; plexi_seat=4; plexi_thk=2; plexi_cl=0.6;
side_fascia_t=3; glue_seat=8; slot=plexi_thk+plexi_cl; ec_len=glue_seat+slot+side_fascia_t;
ci=10.4; cw=2; xin=-15; xout=ci+cw;
gz0 = ec_len - side_fascia_t - slot;
color([0.2,0.7,0.3,0.85])
  translate([xin, -side_fascia_drop-6, gz0 + (slot-plexi_thk)/2])
    cube([xout-xin, (side_fascia_drop+6) + (-oh_under+plexi_seat), plexi_thk]);
