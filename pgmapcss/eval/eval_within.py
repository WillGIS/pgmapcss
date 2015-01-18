class config_eval_within(config_base):
    mutable = 3

def eval_within(param, current):
    if len(param) < 2:
        return ''

    try:
        plan = plpy.prepare('select ST_Within($1, $2) as r', ['geometry', 'geometry'])
        res = plpy.execute(plan, param)
    except Exception as err:
        debug('Eval::within({}): Exception: {}'.format(param, err))
        return ''

    return 'true' if res[0]['r'] else 'false'

# TESTS
# IN ['010200002031BF0D0002000000EC51B89E37753B410AD7A340806D57413333337352753B41D7A3702D836D5741', '010300002031BF0D00010000000500000052B81E458F7C3B41F6285C3FF55E574152B81E458F7C3B41E17A149E468057419A9999198E283C41E17A149E468057419A9999198E283C41F6285C3FF55E574152B81E458F7C3B41F6285C3FF55E5741']
# OUT 'false'
# IN ['010200002031BF0D000700000048E17A14A67D3B413D0AD743DD6F574114AE4721EE7C3B418FC2F53805705741C3F5285CE1793B4148E17A74C6705741B81E856B89793B410AD7A360DB705741AE47E1FAF6783B41713D0A37FE70574185EB51B887773B41713D0A574D715741A4703D8A49753B41000000B0D1715741', '010300002031BF0D00010000000500000052B81E458F7C3B41F6285C3FF55E574152B81E458F7C3B41E17A149E468057419A9999198E283C41E17A149E468057419A9999198E283C41F6285C3FF55E574152B81E458F7C3B41F6285C3FF55E5741']
# OUT 'false'
# IN ['010300002031BF0D000100000007000000EC51B85E25B03B413D0AD7C39D6B57413333337374B03B4166666636A06B574114AE47A10BB13B41333333E3A46B5741A4703D8A1DB13B41CDCCCCCC866B5741666666E6C1B03B41713D0AB7836B5741AE47E1BA34B03B41B81E85FB7F6B5741EC51B85E25B03B413D0AD7C39D6B5741', '010300002031BF0D00010000000500000052B81E458F7C3B41F6285C3FF55E574152B81E458F7C3B41E17A149E468057419A9999198E283C41E17A149E468057419A9999198E283C41F6285C3FF55E574152B81E458F7C3B41F6285C3FF55E5741']
# OUT 'true'