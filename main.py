import ast

import astor


class RewriteImport(ast.NodeTransformer):
    def visit_Import(self, node):
        targets = []
        values = []
        for name in node.names:
            targets.append(
                ast.Name(id=name.asname if name.asname is not None else name.name)
            )
            values.append(
                ast.Call(
                    func=ast.Name(id="__import__"),
                    args=[ast.Constant(name.name)],
                    keywords=[],
                )
            )
        return ast.Assign(
            targets=[ast.Tuple(elts=targets) if len(targets) > 1 else targets[0]],
            value=ast.Tuple(elts=values) if len(values) > 1 else values[0],
        )


if __name__ == "__main__":
    from sys import argv

    with open(argv[1]) as f:
        tree = RewriteImport().visit(ast.parse(f.read()))
    print(astor.to_source(tree))
