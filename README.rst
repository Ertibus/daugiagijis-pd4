Praktinis darbas Nr. 4 - Tesseract
==================================
Table of contents
-----------------
.. contents::


Užduotis
--------
Yra duotas paveikslėlių (.jpg) su tekstu failų archyvas. Iš paveikslėlių reikia „ištraukti“ tekstą ir išsaugoti viename bendrame faile. Teksto „ištraukimui“ iš paveikslėlių galima pasinaudoti Tesseract_ biblioteka.

.. _Tesseract: https://github.com/tesseract-ocr/tesseract

Sukurkite sklandžiai veikiančią daugiagiję *Sender-Receiver* programą, kuri iš pasirinkto katalogo paveikslėlių „ištrauktą“ tekstą apjungtų į vieną failą.

Reikalavimai programai
----------------------

- Programai turi būti pritaikyta *Master-Slave* architektūra, kai Master gija paskirsto darbą Slave gijoms (kiekvienai Slave gijai perduodami 5 paveikslėliai) (**20 taškų**);
- Kiekviena *Slave* gija turi perduoti savo progresą *Master* gijai (**20 taškų**);
- *Slave* gijos turi apdoroti paveikslėlius ir iš jų ištrauktą tekstą perduoti *Master* gijai, kuri gautą tekstą apjungs į vieną failą (**20 taškų**);
- Turi būti rodomas bendras programos progresas: *Slave* gijų progresai, rodomi apdorotų failų bei dar neapdorotų failų sąrašai (**20 taškų**);
- Praradus ryšį su kuria nors *Slave* gija ar įvykus kokiai nors klaidai, tos gijos vykdyta užduotis perduodama kitai *Slave* gijai (**20 taškų**);
- *Slave* gijai atlikus užduotį jai siunčiami kiti 5 paveikslėliai (**10 taškų**);
- *Slave* gijų kiekis gali būti nuo 1 iki begalybės. Kiekviena *Slave* gija turi jungtis prie *Master* gijos (**20 taškų**);

Dependencies
------------
