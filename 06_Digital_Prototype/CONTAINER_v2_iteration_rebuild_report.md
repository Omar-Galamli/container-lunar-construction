# CONTAINER v2 MVP Printable Rebuild Report

This iteration replaces the decorative/full-scale concept with a millimeter-scale MVP test rig.

What was wrong:
- Wheels were too small and not mechanically connected enough for dusty terrain testing.
- The scene had too many sensor bosses for an MVP and several looked like floating clutter.
- The bucket was square and did not include a real lift/curl mechanism.
- Electronics and battery spaces were not designed as printable MVP bays.
- Exterior shield-like panels made the wall busy even though the radiation layer will be added later.
- Robotic arms were visual arms, not clear mechanical linkages with pivots and servo spaces.

What was fixed:
- Rebuilt the body as an open-top 260 x 150 x 108 mm printable shell with a closed front wall.
- Added Arduino UNO tray, 2x18650/small LiPo battery tray, switch mount, charge-port mount, and wire channel.
- Replaced the sensor manifest with 6 minimal sensor sockets and pilot-hole markers.
- Rebuilt wheels as six 74 mm diameter treaded wheels with 3.4 mm axle holes and motor mockup spaces.
- Rebuilt the bucket as a curved scoop with a lift axis and a second under-bucket curl axis.
- Added lift actuator placeholders, curl pushrods, servo pockets, hinge washers, and timeline animation pivots.
- Rebuilt the robotic arms as two exterior rail-mounted linkages with shoulder/elbow/wrist pivots.
- Removed rocks, floating clutter, decorative radiation panels, and the old 48-sensor MVP overload.

Moving parts verified in the model:
- Bucket lift axis: scrub frames 1-100; frame 1 dig, frame 55 lift, frame 100 lift plus curl/dump.
- Bucket second curl axis: under-scoop hinge rotates relative to lift arm for steeper dumping.
- Six wheel bodies: separate printable wheel STLs around 3 mm axle/M3 bolt clearance.
- Left and right exterior robotic arms: shoulder and elbow pivots are keyframed on frames 1-100.

Clearances used:
- Nominal FDM moving clearance: 0.4 mm.
- Hinge/shaft allowance used in holes and washers: 0.6 mm.
- Wheel axle hole: 3.6 mm for a 3.0 mm shaft/M3 bolt.
- Electronics keep-out volumes are visible transparent references and are not exported as print geometry.

Audit result: PASS
- No known fixable issues from the scripted MVP audit.

Exported STL groups:
- `body_fixed.stl` (75 mesh object(s))
- `bucket_lift_arms.stl` (2 mesh object(s))
- `bucket_pushrods.stl` (2 mesh object(s))
- `bucket_scoop.stl` (12 mesh object(s))
- `left_arm_carriage.stl` (1 mesh object(s))
- `left_arm_links.stl` (2 mesh object(s))
- `left_arm_tool.stl` (1 mesh object(s))
- `right_arm_carriage.stl` (1 mesh object(s))
- `right_arm_links.stl` (2 mesh object(s))
- `right_arm_tool.stl` (1 mesh object(s))
- `wheel_left_1.stl` (1 mesh object(s))
- `wheel_left_2.stl` (1 mesh object(s))
- `wheel_left_3.stl` (1 mesh object(s))
- `wheel_right_1.stl` (1 mesh object(s))
- `wheel_right_2.stl` (1 mesh object(s))
- `wheel_right_3.stl` (1 mesh object(s))

Remaining assumptions:
- This is still a Blender MVP prototype, not a stress-checked CAD assembly.
- Use real M3/M4 hardware, shafts, bearings/bushings, and servos/linear actuators for movement tests.
- Before printing, choose final Arduino/battery hardware and adjust tray holes if your exact board/pack differs.
