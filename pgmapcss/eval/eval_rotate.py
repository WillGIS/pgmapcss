def eval_rotate(param):
    if len(param) == 0:
        return ''

    if len(param) == 1:
        return param[0]

    angle = to_float(param[1])
    if angle is None:
        return param[0]

    if len(param) == 2:
        center = eval_centroid([param[0]])
    else:
        center = param[2]

    plan = plpy.prepare('select ST_Translate(ST_Rotate(ST_Translate($1, -X($3), -Y($3)), radians($2)), X($3), Y($3)) as r', ['geometry', 'float', 'geometry'])
    res = plpy.execute(plan, [ param[0], angle, center ])

    return res[0]['r']

# TESTS
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '0']
# OUT '010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641'
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '360']
# OUT '010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641'
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '45']
# OUT '010300002031BF0D0001000000040000008A9ECF32215235412169E48C3EAE5641C6886D281E523541FA17415B3FAE564144725C7E24523541A77403543FAE56418A9ECF32215235412169E48C3EAE5641'
# IN ['010300002031BF0D000100000004000000AE47E1BA1F52354185EB51B83EAE5641C3F528DC1F5235413D0AD7D33FAE5641295C8F4224523541000000B03EAE5641AE47E1BA1F52354185EB51B83EAE5641', '45', '010100002031BF0D008E9ECF32215235412169E48C3EAE5641' ]
# OUT '010300002031BF0D000100000004000000A3C527AE1F52354137FB24693EAE5641DEAFC5A31C52354111AA81373FAE56415C99B4F922523541BD0644303FAE5641A3C527AE1F52354137FB24693EAE5641'

# IN [ '010200002031BF0D00020000008CF0BA3DAD3B3A41F14D01FAA2B55641B071C1489B3B3A41F14D01FAA2B55641', '-159.267477889229', '010100002031BF0D001E313E43A43B3A41F14D01FAA2B55641' ]
# OUT '010200002031BF0D0002000000742599DD9B3B3A41C1ED952EA2B55641C83CE3A8AC3B3A4121AE6CC5A3B55641'
# IN [ '010200002031BF0D00020000007FB2E54FC33B3A4191E01B3EB1B55641A333EC5AB13B3A4191E01B3EB1B55641', '-13.3938031053647' ]
# OUT '010200002031BF0D0002000000126C6111C33B3A41CD7F00B9B0B55641107A7099B13B3A41554137C3B1B55641'
