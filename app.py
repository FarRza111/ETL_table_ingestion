import re
import re
import pandas as pd


BE_PATTERNS =  re.compile(r'\b(LLC|ORG|LIMITED|BV|A\S|LTD|B\.V|Inc\.|INC\.|A\.S|INC|Corp\.|Ltd\.|AG|GmbH|S\.A\.|Pty\ Ltd\.|S\.p\.A\.|B\.V\.|N\.V\.|Co\.|LP|LLP|PC|SARL|SNC|Ltd\.\ Sti\.|Kft\.|Zrt\.|P\.L\.C\.|PLLC|CIC|SpA|Ltda\.|Lda\.|Bhd|AS|AB|ApS|Oy|Oyj|a\.s\.|s\.r\.o\.|d\.o\.o\.|a\.d\.|OU|SIA|UAB|Sarl|SARL|GmbH|PLC|CC|NV|SCA|EEIG|ULC|SAOC|WLL|KSC|PrJSC|PISC|JSC|Ltda|SP|NPO)\b', re.IGNORECASE)



def text_test(text:str):
    removed_chars = text.splitlines(keepends=False)
    rest = " ".join(removed_chars).split()

    temp = {
        "ONLY_ONE_ELEMENT": " ".join(rest) if len(rest) == 1 else "",
        "BIC_XXX": " ".join(rest) if len(rest[0]) == 11 and len(rest) == 1 and rest[0][-3:] == "XXX" else " ",
        "ONLY_TWO_ELEMENTS": " ".join(rest) if len(rest) > 1 and len(rest) < 3 else "",
        "ONLY_3_ELEMENTS": " ".join(rest) if len(rest) == 3 else " ",
        "GR_THAN_3": " ".join(rest) if len(rest) > 3 else " ",
        "ONLY_4_ELEMENTS": " ".join(rest) if len(rest) == 4 else " ",
        "INDIVIDUALS": ",".join(rest) if not all(re.search(BE_PATTERNS, val) for val in removed_chars) and len(rest) == 1 and all(len(val.split(",")) ==2 for val in removed_chars) else " ",
        "BE": " ".join(removed_chars[1:2]) if len(removed_chars) > 1 else (removed_chars[0])

    }

    return temp


if __name__ == "__main__":

    data = pd.read_csv(r'Y:\xBTM\Fariz\data\mt_103_sample_data.csv', usecols=['orderingcustomerdetails', 'orderingcustomername'])

    res = data["orderingcustomername"].apply(lambda x: pd.Series(text_test(x)))
    fulldata = pd.concat([data, res], axis=1)
    fulldata

