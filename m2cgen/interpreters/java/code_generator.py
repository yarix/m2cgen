import contextlib

from m2cgen.interpreters.code_generator import CLikeCodeGenerator


class JavaCodeGenerator(CLikeCodeGenerator):

    scalar_output_type = "double"
    vector_output_type = "double[]"

    def __init__(self, indent=4, is_static_function=True):
        super().__init__(indent)
        self.is_static_method = is_static_function

    def add_class_def(self, class_name, base_class_name, interface_name,
                      modifier="public"):
        if base_class_name is None:
            extends = ""
        else:
            extends = f" extends {base_class_name}"
        if interface_name is None:
            implements = ""
        else:
            implements = f" implements {interface_name}"

        class_def = f"{modifier} class {class_name}{extends}{implements} {{"

        self.add_code_line(class_def)
        self.increase_indent()

    def add_method_def(self, name, args, is_vector_output, modifier="public",
                       is_static_method=True):
        return_type = self._get_var_declare_type(is_vector_output)
        static_key_word = "static " if is_static_method else ""

        func_args = ",".join([
            f"{self._get_var_declare_type(is_vector)} {n}"
            for is_vector, n in args])
        method_def = f"{modifier} {static_key_word}{return_type} " \
                     f"{name}({func_args}) {{"
        self.add_code_line(method_def)
        self.increase_indent()

    def add_package_name(self, package_name):
        self.add_code_line(f"package {package_name};")

    @contextlib.contextmanager
    def class_definition(self, class_name, base_class_name, interface_name):
        self.add_class_def(class_name, base_class_name, interface_name)
        yield
        self.add_block_termination()

    @contextlib.contextmanager
    def method_definition(self, name, args, is_vector_output,
                          modifier="public"):
        self.add_method_def(name, args, is_vector_output, modifier=modifier,
                            is_static_method=self.is_static_method)
        yield
        self.add_block_termination()

    def vector_init(self, values):
        return f"new {self.vector_output_type} {{{', '.join(values)}}}"

    def _get_var_declare_type(self, is_vector):
        return (
            self.vector_output_type if is_vector
            else self.scalar_output_type)

    # Method `function_definition` is required by SubroutinesMixin.
    # We already have this functionality in `method_definition` method.
    function_definition = method_definition
