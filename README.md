# Praktinis darbas Nr. 4
## Užduotis
Yra duotas paveikslėlių (.jpg) su tekstu failų archyvas. Iš paveikslėlių reikia „ištraukti“ tekstą ir išsaugoti viename bendrame faile. Teksto „ištraukimui“ iš paveikslėlių galima pasinaudoti [Tesseract](https://github.com/tesseract-ocr/tesseract) biblioteka.

Sukurkite sklandžiai veikiančią daugiagiję _Sender-Receiver_ programą, kuri iš pasirinkto katalogo paveikslėlių „ištrauktą“ tekstą apjungtų į vieną failą.

## Reikalavimai programai:

- Programai turi būti pritaikyta _Master-Slave_ architektūra, kai Master gija paskirsto darbą Slave gijoms (kiekvienai Slave gijai perduodami 5 paveikslėliai) (__20 taškų__);
- Kiekviena _Slave_ gija turi perduoti savo progresą _Master_ gijai (__20 taškų__);
- _Slave_ gijos turi apdoroti paveikslėlius ir iš jų ištrauktą tekstą perduoti _Master_ gijai, kuri gautą tekstą apjungs į vieną failą (__20 taškų__);
- Turi būti rodomas bendras programos progresas: _Slave_ gijų progresai, rodomi apdorotų failų bei dar neapdorotų failų sąrašai (__20 taškų__);
- Praradus ryšį su kuria nors _Slave_ gija ar įvykus kokiai nors klaidai, tos gijos vykdyta užduotis perduodama kitai _Slave_ gijai (__20 taškų__);
- _Slave_ gijai atlikus užduotį jai siunčiami kiti 5 paveikslėliai (__10 taškų__);
- _Slave_ gijų kiekis gali būti nuo 1 iki begalybės. Kiekviena _Slave_ gija turi jungtis prie _Master_ gijos (__20 taškų__);

## Dependencies
