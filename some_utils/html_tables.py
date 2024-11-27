def make(headers: list[str], data: list[list[str]]) -> str:
    msg = ['<table>', '<tr>',]
    msg += [f"<th>{header}</th>" for header in headers]
    msg += ['</tr>']
    for row in data:
        msg += ['<tr>']
        msg += [f"<td>{cell}</td>" for cell in row]
        msg += ['</tr>']
    msg += ['</table>']
    return '\n'.join(msg)
