import unicodedata
import re
import string


standard_string_with_special_characters = string.punctuation

normal_characters = string.printable + 'áàâãéèêíìîóòôõúùûüç' + 'áàâãéèêíìîóòôõúùûüç'.upper()

standard_list_with_stopwords_for_frequency = ['a','à','as','às','ao','aos','da','das','na','nas','numa','numas',
                                       'o','os','ou','do','dos','no','nos',
                                       'de','e','é','ser','será','serão','são','está','estão','foi','em','num','nuns',
                                       'são','sem','mais','menos',
                                       'um','uma','uns','umas',
                                       'sua','suas','seu','seus',
                                       'nosso','nossos','nossa','nossas',
                                       'esse','esses','essa','essas',
                                       'só','tão','tem','tens','nem','isso','tá','ta','eu','isto','mas',
                                       'sempre','nunca',
                                       'pelo','também','já','você','vocês','vc','vcs',
                                       'ele','eles','ela','elas','nele','neles','nela','nelas',
                                       'se','te','que','por','pro','pros','pra','pras','para','com','como','sobre','sim','não']

standard_list_with_stopwords_for_tokenization = ['a','à','as','às','ao','aos','da','das','na','nas','numa','numas',
                                       'o','os','ou','do','dos','no','nos',
                                       'de','e','em','num','nuns','ser','será','seres',
                                       'se','te','que','por','com','sobre']

standard_list_with_phrases_final_dots = ['.','!','?',';',':']

day_regex_pattern = r'(0?[1-9]|1[0-9]|2[0-9]|3[0-1])'
month_regex_pattern = r'(0?[1-9]|1[0-2])'
year_regex_pattern = r'\d{2,4}'
dates_regex_pattern = r'\b{dia}\/{mes}\/{ano}\b|\b{ano}\/{mes}\/{dia}\b|\b{dia}\-{mes}\-{ano}\b|\b{ano}\-{mes}\-{dia}\b'.format(dia=day_regex_pattern,mes=month_regex_pattern,ano=year_regex_pattern)

emails_regex_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

ddd_county_regex_pattern = r'(\+(\s+)?)?\d{2,3}'
ddd_state_regex_pattern = r'(\((\s+)?)?\d{2}((\s+)?\))?'
ddd_celphones_regex_pattern = r'\d{4,5}([-\s])?\d{4}'
celphones_regex_pattern = r'({pais})?({estado})({celular})|({pais}(\s+)?)?({estado}(\s+)?)({celular})'.format(pais=ddd_county_regex_pattern,estado=ddd_state_regex_pattern,celular=ddd_celphones_regex_pattern)

links_regex_pattern = r'https?://\S+'

numbers_regex_pattern = r'(\b)?\d+(\S+)?(,\d+)?(\b)?|(\b)?\d+(\S+)?(.\d+)?(\b)?'

money_regex_pattern = r'R\$(\s+)?\d+(\S+)?(,\d{2})?|\$(\s+)?\d+(\S+)?(\.\d{2})?'

def colectTextFromTxtFile(file_path : str,
                          encoding_type : str = 'utf-8') -> str | None:
    try:
        with open(file_path,'r',encoding=encoding_type) as f:
            return f.read()
    except Exception as e:
        error = f'{e.__class__.__name__}: {str(e)}'
        print(f'There was an error during the opening process for the file "{file_path}".\n--> {error}')
        return None

def removeSpecialCharacters(text_string : str,                              
                               string_with_special_characters : str = standard_string_with_special_characters,                               
                               remove_extra_blank_spaces : bool = True,
                               remove_hyphen_from_words : bool = False,
                               personalized_treatment : bool = True) -> str:
    """
    Esta função remove characters presentes na lista de characters para remoção fornecida 
    da string de text_string fornecida.
       

    Params
    ----------
    - :paramtext_string: String que você quer limpar dos characters especiais.
    - :paramstring_with_special_characters: String contendo todos os 
    characters especiais que você quer remover da string de text_string fornecida (o 
    padrão é a string "!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~".

    Returns
    --------
    - :return: String fornecida sem os characters especiais.
    """
    if not remove_hyphen_from_words:
        string_with_special_characters = string_with_special_characters.replace('-','')
        text_string = text_string.replace(' -',' ').replace('- ',' ')
    if not personalized_treatment:
        text_string = text_string.translate(str.maketrans('','',string_with_special_characters))
    else:
        # string_with_special_characters_add_space = re.sub(r'\,\.\!|\#|\$|\%|\&\(|\)\+|\-|\?|\@\[|\]|\{|\||\}|\~','',string_with_special_characters)
        if remove_hyphen_from_words:
            string_with_special_characters_add_space = r'\/\\\-'
        else:
            string_with_special_characters_add_space = r'\/\\'
        text_string = text_string.translate(str.maketrans(string_with_special_characters_add_space,' '*len(string_with_special_characters_add_space)))
        text_string = text_string.translate(str.maketrans('','',string_with_special_characters))
    if remove_extra_blank_spaces:
        text_string = removeExtraBlankSpaces(text_string)
    return text_string

def removeMoreThanSpecialCharacters(text_string : str) -> str:
    """
    Esta função passa por todos os characters presentes na string de text_string 
    fornecida e, se o character não estiver dentro da string "normal_characters", 
    a qual é basicamente:
    "string.printable + 'áàâãéèêíìîóòôõúùûç' + 'áàâãéèêíìîóòôõúùûç'.upper()",
    remove-o da string original.

    Params
    ----------
    - :paramtext_string: String contendo o text_string que você quer limpar.

    Returns
    --------
    - :return: String limpa dos characters "mais que especiais" (emojis, dígitos estranhos, 
    formas que não se encontram no teclado, etc).
    """
    for c in text_string:
        if c not in normal_characters:
            text_string = text_string.replace(c,'')
    return text_string

def removeExtraBlankSpaces(text_string : str) -> str:
    transformed_text_string = re.sub(r'[^\S\n]+',' ',text_string)
    return transformed_text_string

def transformTextReplacingCharacters(text_string : str,
                                    characters : str | list[str],
                                    replace_for : str = '',
                                    counting : int = 0,
                                    ignore_case : bool = False) -> str:
    """
    Esta função remove os characters específicos de sua escolha da string de text_string fornecida, 
    com base nas regras que você define usando os Params.

    Params
    ----------
    - :paramtext_string: String contendo o text_string que você quer transformar.
    - :paramcharacters: String contendo o character (ou characters, se for uma palavra) que 
    você deseja substituir.
    - :paramreplace_for: String contendo o character (ou os characters, se for uma palavra) 
    que você deseja botar no lugar dos characters que você deseja substituir.
    - :paramcounting: Número de vezes referente à remoção do(s) character(es) escolhido(s) toda 
    vez que ele for encontrado na string de text_string fornecida (o valor padrão é -1, que indica que 
    serão removidos todas as aparições, mas também poderá ser escolhido como counting = 0 se você 
    quer que seja removido apenas a última aparição). A ordem da counting é sempre do início para o 
    fim da string de text_string.
    - :paramignore_case: Bool que dirá se você quer considerar 
    as letras maiúscula e minúsculas como iguais (True) ou não (False).
    Returns
    --------
    - :return: String fornecida sem os characters escolhidos.
    """
    if isinstance(characters,str):
        for c in characters:
            if c in string.punctuation:
                characters = characters.replace(c,r'\{x}'.format(x=c))
    if counting == -1:        
        if isinstance(characters,str):
            if ignore_case:
                analyzed_text_string = text_string.lower()
                characters = characters.lower()
            else:
                analyzed_text_string = text_string

            result = [indice.start() for indice in re.finditer(r'{}'.format(characters),analyzed_text_string)]
            if result:
                text_string = text_string[:result[-1]]+replace_for+text_string[result[-1]+1:]
            return text_string
        
        elif isinstance(characters,list):
            regex_pattern_characters_in_list = r''
            for character in characters:
                if character in string.punctuation:
                    character = r'\{x}'.format(x=character)
                regex_pattern_characters_in_list += r'{x}|'.format(x=character)
            regex_pattern_characters_in_list = regex_pattern_characters_in_list[0:-1]
            if ignore_case:
                result = [indice.start() for indice in re.finditer(regex_pattern_characters_in_list,text_string,flags=re.IGNORECASE)]
            else:
                result = [indice.start() for indice in re.finditer(regex_pattern_characters_in_list,text_string)]
            if result:
                text_string = text_string[:result[-1]]+replace_for+text_string[result[-1]+1:]
            return text_string
    else:
        if isinstance(characters,str):
            if ignore_case:
                return re.sub(r'{c}'.format(c=characters),replace_for,string=text_string,count=counting,flags=re.IGNORECASE)
            else:
                return re.sub(r'{c}'.format(c=characters),replace_for,string=text_string,count=counting)
        elif isinstance(characters,list):
            regex_pattern_characters_in_list = r''
            for character in characters:
                if character in string.punctuation:
                    character = r'\{x}'.format(x=character)
                regex_pattern_characters_in_list += r'{x}|'.format(x=character)
            regex_pattern_characters_in_list = regex_pattern_characters_in_list[0:-1]
            if ignore_case:
                return re.sub(regex_pattern_characters_in_list,replace_for,string=text_string,count=counting,flags=re.IGNORECASE)
            else:
                return re.sub(regex_pattern_characters_in_list,replace_for,string=text_string,count=counting)

def checkExistenceOfElement(text_string : str,
                                  specific_searched_string : str | None = None,
                                  find_dates : bool = False,                                  
                                  find_emails : bool = False,
                                  find_celphones : bool = False,
                                  find_links : bool = False,
                                  find_numbers : bool = False,
                                  find_money : bool = False,
                                  ignore_case : bool = True) -> bool:
    
    if specific_searched_string:
        for c in specific_searched_string:
            if c in specific_searched_string:
                specific_searched_string.replace(c,r'\{x}'.format(x=c))
        if ignore_case:
            if re.search(r'{x}'.format(x=specific_searched_string),text_string,flags=re.IGNORECASE):
                return True
            else:
                return False
        else:
            if re.search(r'{x}'.format(x=specific_searched_string),text_string):
                return True
            else:
                return False
    if find_dates:
        if re.search(dates_regex_pattern,text_string):
            return True
        else:
            return False
    if find_emails:
        if re.search(emails_regex_pattern,text_string):
            return True
        else:
            return False
    if find_celphones:
        if re.search(celphones_regex_pattern,text_string):
            return True
        else:
            return False
    if find_links:
        if re.search(links_regex_pattern,text_string):
            return True
        else:
            return False
    if find_numbers:
        if re.search(numbers_regex_pattern,text_string):
            return True
        else:
            return False
    if find_money:
        if re.search(money_regex_pattern,text_string):
            return True
        else:
            return False

def standardizeDates(text_string: str,
                    standard_date : str = 'DATA') -> str:
    transformed_text_string = re.sub(dates_regex_pattern,standard_date,text_string)
    return transformed_text_string

def standardizeEmails(text_string : str,
                     standard_email : str = 'EMAIL') -> str:
    transformed_text_string = re.sub(emails_regex_pattern,standard_email,text_string)
    return transformed_text_string

def standardizeCelphones(text_string : str,
                              standard_celphone : str = 'TEL') -> str:
    transformed_text_string = re.sub(celphones_regex_pattern,standard_celphone,text_string)
    return transformed_text_string

def standardizeLinks(text_string : str,
                    standard_link : str = 'LINK') -> str:    
    transformed_text_string = re.sub(links_regex_pattern,standard_link,text_string)
    return transformed_text_string

def standardizeNumbers(text_string : str,
                      standard_number : str = 'NUM') -> str:
    transformed_text_string = re.sub(numbers_regex_pattern,standard_number,text_string)
    return transformed_text_string

def standardizeMoney(text_string : str,
                        standard_money : str = '$') -> str:    
    transformed_text_string = re.sub(money_regex_pattern,standard_money,text_string)
    return transformed_text_string

def standardizeCanonicForm(text_string : str) -> str:
    return ''.join(c for c in (d for char in text_string for d in unicodedata.normalize('NFD', char) if unicodedata.category(d) != 'Mn'))

def standardizeLowerCase(text_string : str) -> str:
    transformed_text_string = text_string.lower()
    return transformed_text_string

# Função auxiliar da função de joinTextWithLineBreaks()
def checkEndOfPhrase(first_line : str,
                          second_line : str,
                          list_of_final_dots : list = standard_list_with_phrases_final_dots) -> tuple[bool, str]:
    for final_dot in list_of_final_dots:
        if first_line.strip().endswith(final_dot):
            return True, second_line
    if first_line.endswith('-') and not (second_line.startswith(' ')):
        return False, first_line+second_line.strip()        
    else:
        return False, first_line.strip()+' '+second_line.strip()

def joinTextWithLineBreaks(text_string : str,
                            return_list_type : bool = False) -> str:
        
    split_text_by_break_line = text_string.split('\n')
    complete_sentences_per_line = []
    
    if split_text_by_break_line:
        complete_sentences_per_line.append(removeExtraBlankSpaces(split_text_by_break_line[0].strip()))    
        for line in split_text_by_break_line[1:]:
            if line.strip() != '':
                line = removeExtraBlankSpaces(line.strip())
                status_final_line, result = checkEndOfPhrase(first_line=complete_sentences_per_line[-1],second_line=line)
                if status_final_line:
                    complete_sentences_per_line.append(result)
                else:
                    complete_sentences_per_line[-1] = result
            else:
                if complete_sentences_per_line[-1].strip()[-1] not in ['.','!','?',';',':']:
                    complete_sentences_per_line[-1] = complete_sentences_per_line[-1].strip() +'.'
    if return_list_type:
        return complete_sentences_per_line
    else:
        return ' '.join(complete_sentences_per_line)

def tokenizeText(text_string : str | list,
                   remove_stopwords : bool = False,
                   list_of_stopwords : list = standard_list_with_stopwords_for_tokenization,
                   disregard_accentuation_on_stopwords : bool = False,
                   standard_treatment : bool = True) -> list:
    if disregard_accentuation_on_stopwords:
        list_of_stopwords = [standardizeCanonicForm(element) for element in list_of_stopwords]

    if standard_treatment:
        if isinstance(text_string,str):
            text_string = removeMoreThanSpecialCharacters(text_string)
            text_string = removeSpecialCharacters(text_string)
            text_string = removeExtraBlankSpaces(text_string)
            text_string = standardizeLowerCase(text_string)
        else:
            list_of_phrases = []
            for element in text_string:
                if isinstance(element,str):
                    element = standardizeLowerCase(element)
                    element = removeMoreThanSpecialCharacters(element)
                    element = removeSpecialCharacters(element)
                    element = removeExtraBlankSpaces(element)
                    list_of_phrases.append(element)
                elif isinstance(element,list):                    
                    secundary_list_of_phrases = []
                    for item in element:                        
                        if isinstance(item,str):
                            item = standardizeLowerCase(item)
                            item = removeMoreThanSpecialCharacters(item)
                            item = removeSpecialCharacters(item)
                            item = removeExtraBlankSpaces(item)
                            secundary_list_of_phrases.append(item)                        
                    list_of_phrases.append(secundary_list_of_phrases)
                
            text_string = list_of_phrases

    if isinstance(text_string,str):
        list_of_tokens = []

        split_text_string = text_string.split()
        if remove_stopwords:
            for token in split_text_string:
                if token not in list_of_stopwords:
                    list_of_tokens.append(token)
        else:
            for token in split_text_string:
                list_of_tokens.append(token)

        return list_of_tokens
    
    else:
        list_of_phrases_com_tokens = []

        for element in text_string:
            if isinstance(element,str):
                list_of_tokens = []
                split_text_string = element.split()
                if remove_stopwords:
                    for token in split_text_string:
                        if token not in list_of_stopwords:
                            list_of_tokens.append(token)
                else:
                    for token in split_text_string:
                        list_of_tokens.append(token)
                list_of_phrases_com_tokens.append(list_of_tokens)
            elif isinstance(element,list):
                if len(element) > 1:
                    secundary_list_of_phrases_com_tokens = []
                    for item in element:
                        if isinstance(item,str):
                            list_of_tokens = []
                            split_text_string = item.split()
                            if remove_stopwords:
                                for token in split_text_string:
                                    if token not in list_of_stopwords:
                                        list_of_tokens.append(token)
                            else:
                                for token in split_text_string:
                                    list_of_tokens.append(token)                        
                            secundary_list_of_phrases_com_tokens.append(list_of_tokens)
                    list_of_phrases_com_tokens.append(secundary_list_of_phrases_com_tokens)
                else:
                    for item in element:
                        if isinstance(item,str):
                            list_of_tokens = []
                            split_text_string = item.split()
                            if remove_stopwords:
                                for token in split_text_string:
                                    if token not in list_of_stopwords:
                                        list_of_tokens.append(token)
                            else:
                                for token in split_text_string:
                                    list_of_tokens.append(token)                        
                            list_of_phrases_com_tokens.append(list_of_tokens) 

        return list_of_phrases_com_tokens

def countWordsFrequency(text_string : str | list,
                        specific_words : list[str] | None = None,
                        n_top : int = -1,
                        remove_stopwords : bool = True,
                        list_of_stopwords : list = standard_list_with_stopwords_for_frequency,
                        standard_treatment : bool = True) -> list:    

    tokenized_list = tokenizeText(text_string=text_string,remove_stopwords=remove_stopwords,list_of_stopwords=list_of_stopwords,standard_treatment=standard_treatment)
    dic = {}
    if specific_words:
        if isinstance(tokenized_list[0],str):
            for word in specific_words:
                if word not in dic.keys():
                    dic[word] = tokenized_list.count(word)
        elif isinstance(tokenized_list[0],list):
            for sentence in tokenized_list:
                used_words = []
                for word in specific_words:
                    if word not in used_words:
                        if word not in dic.keys():
                            dic[word] = sentence.count(word)
                    else:
                        dic[word] += sentence.count(word)

    else:
        if tokenized_list:
            if isinstance(tokenized_list[0],str):
                for token in tokenized_list:
                    if token not in dic.keys(): # maybe we could use ".count()" instead of these huge loop!
                        dic[token] = 1
                    else:
                        dic[token] += 1
            elif isinstance(tokenized_list[0],list):
                for sentence in tokenized_list:
                    for token in sentence:                        
                        if token not in dic.keys():
                            dic[token] = 1
                        else:
                            dic[token] += 1
    frequency_list = []
    for token in dic.keys():
        token_frequency = dic[token]
        frequency_list.append((token,token_frequency))
    
    frequency_list = sorted(frequency_list, key=lambda x: x[1], reverse=True)

    if n_top != -1:
        frequency_list = frequency_list[:n_top]
    # sortar a lista para maior pra menor e depois ver se precisa restringir o result pros top

    return frequency_list

def formatText(text_string : str,
                standardize_lower_case : bool = True,
                remove_morethanspecial_characters : bool = True,
                remove_special_characters : bool = True,
                string_with_special_characters : str = standard_string_with_special_characters,
                remove_extra_blank_spaces : bool = True,
                standardize_links : bool = False,
                standard_link : str = 'LINK',
                standardize_numbers : bool = False,
                standard_number : str = 'NUM',
                standardize_money : bool = False,
                standard_money : str = '$',
                standardize_dates : bool = False,
                standard_date : str = 'DATA',
                standardize_emails : bool = False,
                standard_email : str = 'EMAIL',
                standardize_celphones : bool = False,
                standard_celphone : str = 'TEL',
                standardize_canonic_form : bool = False) -> str:
    if remove_morethanspecial_characters:
        text_string = removeMoreThanSpecialCharacters(text_string)
    if standardize_money:
        for character_standard_money in standard_money:
            if character_standard_money in string_with_special_characters:
                special_characters_impact_standard_money = True
                text_string = standardizeMoney(text_string=text_string,standard_money='codpdintzzqaio')
                break
        else:
            special_characters_impact_standard_money = False
            text_string = standardizeMoney(text_string=text_string,standard_money=standard_money)    
    if standardize_links:
        for character_standard_link in standard_link:
            if character_standard_link in string_with_special_characters:
                special_characters_impact_standard_link = True
                text_string = standardizeLinks(text_string=text_string,standard_link='codpltzzqaio')
                break
        else:
            special_characters_impact_standard_link = False
            text_string = standardizeLinks(text_string=text_string,standard_link=standard_link)    
    if standardize_dates:
        for character_standard_date in standard_date:
            if character_standard_date in string_with_special_characters:
                special_characters_impact_standard_date = True
                text_string = standardizeDates(text_string=text_string,standard_date='codpdttzzqaio')
                break
        else:
            special_characters_impact_standard_date = False
            text_string = standardizeDates(text_string=text_string,standard_date=standard_date)
    if standardize_emails:
        for character_standard_email in standard_email:
            if character_standard_email in string_with_special_characters:
                special_characters_impact_standard_email = True
                text_string = standardizeEmails(text_string=text_string,standard_email='codpemtzzqaio')
                break
        else:
            special_characters_impact_standard_email = False
            text_string = standardizeEmails(text_string=text_string,standard_email=standard_email)
    if standardize_celphones:
        for character_standard_celphone in standard_celphone:
            if character_standard_celphone in string_with_special_characters:
                special_characters_impact_standard_celphone = True
                text_string = standardizeCelphones(text_string=text_string,standard_celphone='codptctzzqaio')
                break
        else:
            special_characters_impact_standard_celphone = False
            text_string = standardizeCelphones(text_string=text_string,standard_celphone=standard_celphone)
    if standardize_numbers:
        for character_standard_number in standard_number:
            if character_standard_number in string_with_special_characters:
                special_characters_impact_standard_number = True
                text_string = standardizeNumbers(text_string=text_string,standard_number='codpntzzqaio') 
                break
        else:
            special_characters_impact_standard_number = False
            text_string = standardizeNumbers(text_string=text_string,standard_number=standard_number)

    if remove_special_characters:
        text_string = removeSpecialCharacters(text_string=text_string,
                                           string_with_special_characters=string_with_special_characters)
    if standardize_canonic_form:
        text_string = standardizeCanonicForm(text_string)
    if remove_extra_blank_spaces:
        text_string = removeExtraBlankSpaces(text_string)
    if standardize_lower_case:
        text_string = standardizeLowerCase(text_string)
    if standardize_money and special_characters_impact_standard_money:
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codpdintzzqaio',replace_for=standard_money)
    if standardize_links and special_characters_impact_standard_link:
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codpltzzqaio',replace_for=standard_link)
    if standardize_numbers and special_characters_impact_standard_number: 
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codpntzzqaio',replace_for=standard_number)
    if standardize_dates and special_characters_impact_standard_date:
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codpdttzzqaio',replace_for=standard_date)
    if standardize_emails and special_characters_impact_standard_email:
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codpemtzzqaio',replace_for=standard_email)
    if standardize_celphones and special_characters_impact_standard_celphone:
        text_string = transformTextReplacingCharacters(text_string=text_string,characters='codptctzzqaio',replace_for=standard_celphone)
    
    return text_string
