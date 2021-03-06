class config_eval_div(config_base):
    math_level = 4
    op = '/'
    def mutable(self, param_values, stat):
        import pgmapcss.eval
        config_metric = pgmapcss.eval.eval_functions.list()['metric']
        ret = [ config_metric.mutable([p], stat) for p in param_values ]
        return min(ret)

def eval_div(param):
  ret = None

  for p in param:
      if p == '' or p == None:
          f = ''
      else:
          f = eval_metric([p])

      f = float(f) if f != '' else 0.0

      if ret is None:
          ret = f
      elif f == 0:
          return ''
      else:
          ret = ret / f

  return float_to_str(ret)

# TESTS
# IN ['5', '1']
# OUT '5'
# IN ['5', '2']
# OUT '2.5'
# IN ['5', '0']
# OUT ''
# IN ['-5', '2']
# OUT '-2.5'
# IN ['6', '4', '2']
# OUT '0.75'
