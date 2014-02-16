class InteractiveExecuteHandler(BaseRequestHandler):
  """Executes the Python code submitted in a POST within this context.

  For obvious reasons, this should only be available to administrators
  of the applications.
  """

  PATH = InteractivePageHandler.PATH + '/execute'

  def post(self):
    save_stdout = sys.stdout
    results_io = cStringIO.StringIO()
    try:
      sys.stdout = results_io

      code = self.request.get('code')
      code = code.replace("\r\n", "\n")

      try:
        compiled_code = compile(code, '<string>', 'exec')
        exec(compiled_code, globals())
      except Exception, e:
        traceback.print_exc(file=results_io)
    finally:
      sys.stdout = save_stdout

    results = results_io.getvalue()
    self.generate('interactive-output.html', {'output': results})
    