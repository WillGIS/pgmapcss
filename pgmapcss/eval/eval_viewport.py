class config_eval_viewport(config_base):
    mutable = 2

def eval_viewport(param, current):
    return render_context['bbox']

# TESTS
# IN []
# OUT '010300002031BF0D000100000005000000DBF1839BB5DC3B41E708549B2B705741DBF1839BB5DC3B41118E9739B171574182069214CCE23B41118E9739B171574182069214CCE23B41E708549B2B705741DBF1839BB5DC3B41E708549B2B705741'
