from bs4 import BeautifulSoup
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
import tqdm
import lxml
import cchardet

POS = {'na': 'N', 'v': 'V', 'vu': '', 'ab': 'V.CVB;NFIN', 'uf': '', 'iiv': 'N;IIV', 'iic': 'N;IIC', 'iip': 'N;IIP', 'pa': 'V.PTCP'}
FEAT = {
    # metalinguistic properties
    'na': '', 'kr': '',
    # number
    'sg': 'SG', 'du': 'DU', 'pl': 'PL',
    # gender
    'mas': 'MASC', 'neu': 'NEU', 'fem': 'FEM', 'dei': '{MASC/FEM/NEU}',
    # case
    'loc': 'LOC', 'acc': 'ACC', 'gen': 'GEN', 'abl': 'ABL',
    'nom': 'NOM', 'dat': 'DAT', 'ins': 'INS', 'voc': 'VOC',
    # conjugational class
    'cj': '',
    'prim': 'IND', 'ca': 'CAUS', 'int': 'INTENS', 'des': 'DESID',
    # TAM
    'sys': '', 'tp': '',
    'prs': 'PRES', 'pef': 'FUT;RMT', 'fut': 'FUT', 'prf': 'PRF',
    'md': '',
    'ip': 'IMP', 'pr': '', 'op': 'OPT', 'im': 'IPFV', 'aor': 'PFV',
    'cnd': 'COND', 'inj': 'INJ', 'ben': 'BEN', 'subj': 'SUBJ',
    # voice
    'para': 'ACT', 'atma': 'MID', 'pass': 'PASS',
    'pas': 'PASS',
    # person
    'np': '',
    'fst': '1', 'snd': '2', 'trd': '3',
    # participles
    'pa': '',
    'no': 'V.PTCP',
    'ppp': 'PASS;PST', 'ppa': 'ACT;PST', 'ppr': 'ACT;PRES', 'pprp': 'PASS;PRES',
    'ppft': 'PRF', 'pfut': 'FUT', 'pfutp': 'PASS;FUT',
    'gya': '', 'iya': '', 'tav': '',
    # non-finite
    'iv': '',
    'inf': 'V;NFIN', 'abs': 'V.CVB;NFIN', 'per': '?',
    # indec
    'ind': 'ADV',
    'avya': 'ADV',
    'interj': 'INTJ',
    'parti': 'PART',
    'prep': 'ADP',
    'conj': 'CONJ',
    'tasil': 'ADV'
}

output = []
pbar = tqdm.tqdm(total=1189184)
with open('SL_morph.xml', 'r') as fin, open('san2', 'w') as fout:
    try:
        for i, row in enumerate(fin):
            # if i < 884000:
            #     continue
            form = BeautifulSoup(row, 'lxml').find('f')

            inflected = form['form']
            inflected = transliterate(inflected, sanscript.SLP1, sanscript.DEVANAGARI)
            lemma = form.find('s')
            if lemma:
                lemma = lemma['stem']
                lemma = transliterate(lemma, sanscript.SLP1, sanscript.DEVANAGARI)
            else:
                lemma = inflected
            lemma = lemma.split('#')[0]

            for entry in form.children:
                if entry.name == 's':
                    continue
                feats = [POS[entry.name]]
                for feature in entry.descendants:
                    if FEAT[feature.name] != '': feats.append(FEAT[feature.name])
                output.append(f'{lemma}\t{inflected}\t{";".join(feats)}\n')

            pbar.update(1)
    except Exception as e:
        print(e, lemma, inflected, form)
        fout.write(''.join(output))
    fout.write(''.join(output))