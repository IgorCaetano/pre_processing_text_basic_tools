
# Toolkit for basic Natural Language Processing processes

This package is a toolkit (multiple def functions) for executing basic process related to initial steps on Natural Language Processing. It's aimed for portuguese BR language usage.

<details>
  <summary><b>Portuguese version  <i>(click to expand)</i></b></summary>
  <br><ul>
  <li><i><a href="https://pypi.org/project/pre-processing-text-basic-tools-br/">Pypi package portuguese version</a></i></li>
  <li><i><a href="https://github.com/IgorCaetano/pre_processing_text_basic_tools_br">GitHub repository portuguese version</a></i></li></ul>
</details>


## 🤩 Functionalities

- Cleaning text;
- Text analysis;
- Text pre-processing for subsequent insertion into natural language training models;
- Easy integration with other Python programs by importing the desired module(s) or function.


## 📦 Installation

This package is installed using the command "*pip install*"

```bash
pip install pre-processing-text-basic-tools
```

## 📜 Usage/Examples

### Removing simple special characters

```python
from pre_processing_text_basic_tools import removeSpecialCharacters

text = "This is an exa@mple of $text? with special# character.s. I want to clean it!!!"

cleaned_text = removeSpecialCharacters(text)

print(cleaned_text)



>>>"This is an example of text with special characters I want to clean it"
```

<details>
  <summary>Important note about hyphenated words  <i>(click to expand)</i></summary>
  <br>
  It is important to highlight that the functions were designed for direct applications in the Portuguese language. Therefore, words with a hyphen, such as "sexta-feira", do not have their special character "-" removed by default, but you can choose to remove the hyphens from such words using the <i>remove_hyphen_from_words</i> parameter, passing it to <i>True</i>. Furthermore, if you want hyphens not to be replaced by a space " ", you can pass the parameter <i>personalized_treatment</i> to <i>False</i>, which replaces characters "/", "\ " is for " ".
  <br><br>
  
  ```python
  from pre_processing_text_basic_tools import removeSpecialCharacters

  text = "Today is sexta-feira and 03/09/2024! Or even 03-09-2024."

  cleaned_text = removeSpecialCharacters(text,remove_hyphen_from_words=True)

  print(cleaned_text)



  >>>"Today is sexta feira and 03 09 2024 Or even 03 09 2024"
  ```
</details>




### Full text formatting and standardization

```python
from pre_processing_text_basic_tools import formatText


text = "This is an example, of $text? I want/ t.o# format and&*. standardize!?"

formatted_text = formatText(text_string=text,
                            standardize_lower_case=True,
                            remove_special_characters=True,
                            remove_morethanspecial_characters=True,
                            remove_extra_blank_spaces=True,
                            standardize_canonic_form=True)

print(formatted_text)



>>>"this is an example of text I want to format and standardize"
```

### Standardization of diverse elements

```python
from pre_processing_text_basic_tools import formatText

text = '''If I have a text with an email like esteehumemail@gmail.com or
noreply@hotmail.com or even emaildeteste@yahoo.com.br.
In addition, I will also have several telephone numbers such as +55 48 911223344 or
4890011-2233 and why not a landline like 48 0011-2233?
You can also have dates such as 12/12/2024 or 2023-06-12 in different types
type 1/2/24
What if the text has a lot of money involved? We are talking about R$200,000.00 or
R$200.00 or even with
the wrong formatting like R$2500!
Furthermore we can simply standardize numbers like 123123 or 24 or
129381233 or even 1,200,234!'''

formatted_text = formatText(text_string=text,                                        
                            standardize_canonic_form=True,
                            standardize_dates=True,
                            standard_date='_data_',
                            standardize_money=True,
                            standard_money='$',
                            standardize_emails=True,
                            standard_email='_email_',
                            standardize_celphones=True,
                            standard_celphone='_tel_',
                            standardize_numbers=True,
                            standard_number='0',
                            standardize_lower_case=True)

print(formatted_text)



>>>"""if i have a text with an email like _email_ or
_email_ or even _email_
in addition i will also have several telephone numbers such as _tel_ or
_tel_ and why not a landline like _tel_
you can also have dates such as _data_ or _data_ in different types
type _data_
what if the text has a lot of money involved we are talking about $ or
$ or even with
the wrong formatting like $
furthermore we can simply standardize numbers like 0 or 0 or
0 or even 0"""
```

### Text tokenization

Basic tokenization

```python
from pre_processing_text_basic_tools import tokenizeText

text = '''This is another example text for tokenization!!! Let's use characters,
specials# too @igorc.s and $follow there?!'''

tokenization = tokenizeText(text)

print(tokenization)



>>>['this', 'is', 'another', 'example', 'text', 'for', 'tokenization', 'lets', 
'use', 'characters', 'specials', 'too', 'igorcs', 'and', 'follow', 'there']
```

# 

<details>
  <summary>Tokenization removing stopwords  <i>(click to expand)</i></summary>
  <br>
  Stopwords are words that do not have much meaning in sentences, so some applications, in order to optimize their processing and training time, remove such words from the text corpus. Some examples of common stopwords are articles and prepositions.
  <br>

  ```python
  from pre_processing_text_basic_tools import tokenizeText

  text = '''O menino gosta de comer frutas e verduras!'''

  tokenization = tokenizeText(text,remove_stopwords=True)

  print(tokenization)



  >>>['menino', 'gosta', 'comer', 'frutas', 'verduras']
  ```

</details>

# 

<details>
  <summary>Tokenization removing stopwords with custom stopwords list  <i>(click to expand)</i></summary>
  <br>
  We can also select a personalized list of stopwords, adding or removing from the default list <i>standard_list_with_stopwords_for_tokenization</i> or even creating a completely unique list.
  <br>

  ```python
  from pre_processing_text_basic_tools import tokenizeText
  from pre_processing_text_basic_tools import standard_list_with_stopwords_for_tokenization

  text = '''This is an example of usage! That is cool for some people, but not for others.'''

  custom_stopwords_list = standard_list_with_stopwords_for_tokenization + ['the','a','an','for','this','that','of','is']

  tokenization = tokenizeText(text_string=text,
                              remove_stopwords=True,
                              list_of_stopwords=custom_stopwords_list)

  print(tokenization)



  >>>['example', 'usage', 'cool', 'some', 'people', 'but', 'not', 'others']
  ```

</details>

# 

<details>
  <summary>More complete tokenization  <i>(click to expand)</i></summary>
  <br>
  You can also use prior formatting before the tokenization process. In the example below, the text is passed into canonical form before tokenizing it. In other words, words like "coração" become "coracao", losing their accents, "ç", etc.
  <br>
    
  ```python
  from pre_processing_text_basic_tools import tokenizeText,formatText

  text = "Este é um exemplo para a ficção científica. Vôo alto! Açaí é bom demais!"

  formatted_text = formatText(text_string=text,standardize_canonic_form=True)

  tokenization = tokenizeText(text_string=formatted_text,
                              remove_stopwords=True)

  print(tokenization)



  >>>['este', 'um', 'exemplo', 'para', 'ficcao', 'cientifica', 'voo', 'alto', 
  'acai', 'bom', 'demais']
  ```

</details>




## 😁 Authors

- [@IgorCaetano](https://github.com/IgorCaetano)


## 🤝 Used by

- This project is used in the text pre-processing stage in the **[WOKE](https://github.com/iaehistoriaUFSC/Repositorio_UFSC)** project of the Grupo de Estudos e Pesquisa em IA e História ("Study and Research Group on AI and History") at UFSC ("Federal University of Santa Catarina").
