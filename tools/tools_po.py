"""最小の .po の読み書き(外部ライブラリなし)。msgid が複数行でも扱える。"""
import re
_ESC = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
def _u(s):
    # 1 文字ずつ、1 回だけ展開する(\\n を、バックスラッシュ + n として正しく扱う)
    import re
    return re.sub(r'\\(.)', lambda m: _ESC.get(m.group(1), '\\' + m.group(1)), s)
def q(s):
    return s.replace('\\','\\\\').replace('"','\\"').replace('\n','\\n').replace('\t','\\t')
def parse(path):
    text=open(path,encoding='utf-8').read()
    blocks=re.split(r'\n\n+',text.strip('\n'))
    entries=[]
    for b in blocks:
        lines=b.split('\n')
        e={'raw':b,'comments':[l for l in lines if l.startswith('#')],'msgid':None,'msgstr':None}
        cur=None;ids=[];strs=[]
        for l in lines:
            if l.startswith('msgid '): cur=ids; cur.append(l[6:])
            elif l.startswith('msgstr '): cur=strs; cur.append(l[7:])
            elif l.startswith('"') and cur is not None: cur.append(l)
        if ids:
            e['msgid']=''.join(_u(re.match(r'"(.*)"$',x).group(1)) for x in ids)
            e['msgstr']=''.join(_u(re.match(r'"(.*)"$',x).group(1)) for x in strs)
        entries.append(e)
    return entries
def render_entry(e,msgstr):
    cm='\n'.join(e['comments'])
    mid=e['msgid']
    def fmt(k,v):
        parts=v.split('\n')
        if len(parts)==1: return f'{k} "{q(v)}"'
        out=[f'{k} ""']
        for i,p in enumerate(parts):
            out.append('"'+q(p)+('\\n' if i<len(parts)-1 else '')+'"')
        return '\n'.join(out)
    # 末尾が空の分割を除く
    return (cm+'\n' if cm else '')+fmt('msgid',mid)+'\n'+fmt('msgstr',msgstr)
