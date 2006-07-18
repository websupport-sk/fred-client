��    �      4  �   L
      �  �   �  C  k  �   �  B  v  �  �  �  h  �     '   �  *   �     �     �     �          "     B  .   ]     �     �     �  
   �  5   �          &     8  -   V     �  ,   �  ,   �     �            *     D   F     �  "   �     �  T   �     ,     G  
   X  o   c  <   �  #        4  3   H  /   |     �     �     �  $   �  $     "   1  "   T     w     �     �     �  	   �     �  '   �  #     	   *     4  '   <  	   d  $   n     �     �     �     �     �              F   ,   M   s   U   �   E   !  s   ]!  I   �!  M   "  H   i"  !   �"  X   �"     -#     1#  H   6#  C   #     �#     �#     �#     $     $     /$     G$  e   M$  @   �$     �$     �$  ,   
%  &   7%     ^%     {%  <   �%  ?   �%     &  G   '&     o&     �&     �&     �&     �&     �&  
   �&     �&     �&     �&     �&     �&     	'     '     $'     2'     M'     ['     r'  
   ~'  '   �'     �'  #   �'     �'     �'     (     (     (      (  
   .(     9(     S(     \(     n(     w(  &   ~(     �(     �(     �(  
   �(  0   �(  
   )     )     $)     -)     0)     7)     D)     V)     e)  	   z)     �)  
   �)     �)  	   �)     �)  .  �)  Q   �*  �   H+  �   ,     �,  �  �-  T  z/  �   �4  :   x5  /   �5     �5     �5     6     $6  $   66  $   [6  /   �6     �6  $   �6     �6     7  5    7     V7     k7  0   ~7  J   �7     �7  )   8  1   68     h8     �8  
   �8  @   �8  B   �8  "   &9  3   I9     }9  �   �9     $:     >:  	   P:  �   Z:  F   �:  +   ,;     X;  ;   q;  1   �;     �;     �;     <  &   $<  (   K<  &   t<  &   �<     �<     �<     �<  
   =     =     +=      >=  )   _=     �=     �=  ,   �=  	   �=  6   �=     >     5>  !   E>     g>     �>     �>  !   �>  Q   �>  O   %?  Q   u?  K   �?  �   @  R   �@  W   A  H   \A     �A  [   �A     !B     (B  b   0B  O   �B     �B     �B     C     (C     CC  $   bC  	   �C  q   �C  J   D     ND     RD  C   mD  (   �D     �D     �D  =   E  ;   FE     �E  Q   �E     �E  
   �E     	F     F     F     %F  
   -F     8F  
   HF     SF     mF     ~F     �F     �F     �F     �F     �F     �F     
G     G  $   G  
   BG  4   MG  $   �G     �G     �G     �G     �G     �G     �G     �G  
   H     H     )H     /H  ,   7H     dH     pH     uH     �H  <   �H     �H     �H     �H     �H     I     I     I     ,I     EI     MI     TI     hI     tI     �I     �I         J       �   4   $   K   k       N   E   l   ^      �      s   <   �   M   �   d          p      
               @   ,   /   U   �   ]              G          �               9              %   H   Z   m       �      �          g   c   V   �   �   ?       X   "       |   �   �   :      5   `           �   �   r   =   Q       �   #                 S   C   D   '   �   �       �   �           ~       b      �   Y      �   I            R   7   j   z   [                           q   a   _   �   e   (   i               !   8      2   �   �       �           n      O       u      x       B              6       �   L           3   >   0       y   �       A           .   +   *   �       �   1   \   )   �          T   t           �   {   F         	      P       h      �   �             }      ;       v   �   w   o   &   W       �   -   �           f    
   The "login" command establishes an ongoing server session that preserves client identity
   and authorization information during the duration of the session. 
   The EPP "check" command is used to determine if an object can be
   provisioned within a repository.  It provides a hint that allows a
   client to anticipate the success or failure of provisioning an object
   using the "create" command as object provisioning requirements are
   ultimately a matter of server policy.
 
   The EPP "create" command is used to create an instance of an object.
   An object can be created for an indefinite period of time, or an
   object can be created for a specific validity period.
 
   The EPP "info" command is used to retrieve information associated
   with an existing object. The elements needed to identify an object
   and the type of information associated with an object are both
   object-specific, so the child elements of the <info> command are
   specified using the EPP extension framework.
 
   The EPP "transfer" command provides a query operation that allows a
   client to determine real-time status of pending and completed
   transfer requests.
   The EPP "transfer" command is used to manage changes in client
   sponsorship of an existing object.  Clients can initiate a transfer
   request, cancel a transfer request, approve a transfer request, and
   reject a transfer request using the "op" command attribute.
 
${BOLD}${GREEN}Session commands:${NORMAL}
${BOLD}connect${NORMAL} (or directly login) ${CYAN}# connect to the server (for test only)${NORMAL}
${BOLD}lang${NORMAL} cs ${CYAN}# set language of the incomming server messages. It MUST be set BEFORE send login! Later has no effect.${NORMAL}
${BOLD}validate${NORMAL} [on/off] ${CYAN}# set validation or display actual setting${NORMAL}
${BOLD}poll-ack${NORMAL} [on/off] ${CYAN}# send "poll ack" straight away after "poll req"${NORMAL}
${BOLD}raw-c${NORMAL}[ommand] [xml]/${BOLD}d${NORMAL}[ict] ${CYAN}# display raw command${NORMAL} (instead of raw you can also type ${BOLD}src${NORMAL})
${BOLD}raw-a${NORMAL}[nswer] [xml]/${BOLD}d${NORMAL}[ict]  ${CYAN}# display raw answer${NORMAL}
${BOLD}confirm${NORMAL} ${BOLD}on${NORMAL}/[off]  ${CYAN}# confirm editable commands befor sending to the server${NORMAL}
${BOLD}config${NORMAL} ${CYAN}# display actual config${NORMAL}
${BOLD}config${NORMAL} ${BOLD}create${NORMAL} ${CYAN}# create default config file in user home folder.${NORMAL}
${BOLD}send${NORMAL} [filename] ${CYAN}# send selected file to the server (for test only). If param is not valid file the command shows folder.${NORMAL}
 ${BOLD}${YELLOW}Start interactive input of params. To break type: ${NORMAL}${BOLD}!${NORMAL}[!!...] (one ${BOLD}!${NORMAL} for scope) (Value can be a list of max %d values.) (Value can be an unbouded list of values.) Actual config is Answer source Available EPP commands Available values Certificate key file not found. Certificate names not set. Certificates missing. Try connect without SSL! Command source Command was sent to EPP server. Confirm has been set to Confirm is Connected to host ${GREEN}${BOLD}%s${NORMAL}, port %d Connection broken Connection closed Create default config failed. Default config file saved. For more see help. Dir list Do you want send this command to the server? Document has wrong encoding. LookupError: %s EPP document is not valid Example of input Examples Fatal error: Create default config failed. For connection to the EPP server type "connect" or directly "login". For disable validator type For help type "help" (or "h", "?") For more type For stop interactive input type ! instead of value (or more "!" for leave sub-scope) Greeting message incomming Help for command IP address If this script runs under MS Windows and timeout is not zero, it is probably SLL bug! Set timeout back to zero. Impossible create connection. Required config values missing Impossible saving conf file. Reason Init SSL connection Instead "command" Select one from this list bellow: Internal Error: Master node '%s' doesn't exist. Interpreted answer Interpreted command Interrupt from user Invalid XML document. ExpatError: %s Invalid bracket definition (childs). Invalid bracket definition (list). Invalid bracket definition (mode). Invalid input format. Invalid parameter index Invalid response code LIST of DNS Load file Login failed Missing result in the response message. Missing values. Required minimum is No config No data No response. EPP Server doesn't answer. Not found Param MUST be a value from this list Private key file not found. Send logout Server answer is not valid! Session language is Session language was set to Start session! Status: Validation is Temporary file for verify XML EPP validity cannot been created. Reason The EPP "delete" command is used to remove an instance of an existing object. The EPP "hello" request a "greeting" response message from an EPP server at any time. The EPP "logout" command is used to end a session with an EPP server. The EPP "poll" command is used to discover and retrieve service messages queued by a server for individual clients. The EPP "renew" command is used to extend validity of an existing object. The EPP "update" command is used to update an instance of an existing object. The server configuration is not valid. Contact the server administrator. This language code is not allowed To start the interactive mode of input the command params type: ${BOLD}!command${NORMAL} Try Type Type "?command" (or "h(elp) command") for mode details about parameters. Unknown EPP command. Select one from EPP commands list (Type help). Unknown EPP command: %s. Unknown command Unknown language code Unknown parameter name Unknown response type Unknown server response Usage Usage: python ccreg_console.py [host] [lang] # (lang is only cs/en and it can be also set befor host) Used certificat is not signed by verified certificate authority. VAT Validation is set Validator has been disabled. For enable type Value "%s" is not allowed here. Valid: Welcome to the ccReg console You are logged already. You are not connected! For connection type: connect or login You are not connected! Type login for connection to the server. You are not connected. You are not logged. You must call login() before working on the server. accept only values add part address change part city contact contact ID contact name country code current expiration date disclose address disclose email disclose fax disclose flag disclose name disclose organisation name disclose part disclose voice (phone) domain name fax number index of message, required with op=ack! list of DNS list of values overflow. Maximum is list with max %d items. missing name new password notify email nsset address nsset name number of months or years optional organisation name password period period unit (y year(default), m month) poll ack is postal code postal informations query type readline module missing - cmd history is diabled registrant remove part required sp street tech contact technical contact unbounded list voice (phone number) your city your contact ID your email your login name your name your password Project-Id-Version: 1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2006-07-18 11:31+0200
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: Zdeněk Böhm <zdenek.bohm@nic.cz>
Language-Team: CS <info@nic.cz>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
 
EPP příkaz "login" identifikuje uživatele a zahájí spojení s EPP serverem. 
   EPP Příkaz "check" se používá ke zjištění jestli se daný objekt
   v repozitáři nachází. To umožňuje řídit spouštění příkazu "create"
   a poté vyhodnotit jestli příkaz uspěl nebo ne.
 
   EPP příkaz "create" se používá pro vytvoření instance objektu.
   Objekt může být vytvořen na neučitý časový úsek nebo na přesně
   definované období.
 
   EPP příkaz "info" se používá ke zjištění informací spojených
   s vybraným objektem. Způsob identifikace objektu a typu
   navrácených informací spojených s objektem závisí na konkrétním
   typu info příkazu a případném použití EPP extension rozšíření.
 
   EPP příkaz "transfer" umožňuje zjišťovat aktuální stav
   nevyřízených anebo dokončených požadavků na transfer.
   Příkaz "transfer" se používá k ovládání změn
   na vybraném objektu. Klient může vyvolat požadavek
   na transfer. Nebo může požadovat zrušení požadavku, potvrzení
   požadavku a nebo odebrání požadavku. To vše pomocí atributu "op".
 
${BOLD}${GREEN}Příkazy relace (session):${NORMAL}
${BOLD}connect${NORMAL} (nebo přímo login) ${CYAN}# připojení k serveru(jen pro testování)${NORMAL}
${BOLD}lang${NORMAL} cs ${CYAN}# nastavení jazyka, kterým bude server odpovídat.MUSÍ být nastaven PŘED odesláním login! Pak již nemá žádný efekt.${NORMAL}
${BOLD}validate${NORMAL} [on/off] ${CYAN}# nastavení validace nebo zjištění aktuálního stavu${NORMAL}
${BOLD}poll-ack${NORMAL} [on/off] ${CYAN}# pošle "poll ack" hned za příkazem "poll req"${NORMAL}
${BOLD}raw-c${NORMAL}[ommand] [xml]/${BOLD}d${NORMAL}[ict] ${CYAN}# zobrazit zdrojový tvar příkazu${NORMAL} (místo raw můžete zadat také ${BOLD}src${NORMAL})
${BOLD}raw-a${NORMAL}[nswer] [xml]/${BOLD}d${NORMAL}[ict]  ${CYAN}# zobrazit zdrojový tvar odpovědi${NORMAL}
${BOLD}confirm${NORMAL} ${BOLD}on${NORMAL}/[off]  ${CYAN}# potvrzení editačních příkazů před odesláním na server${NORMAL}
${BOLD}config${NORMAL} ${CYAN}# zobrazení aktuálních hodnot v config souboru (nebo defaultu)${NORMAL}
${BOLD}config${NORMAL} ${BOLD}create${NORMAL} ${CYAN}# vytvoření defaultního config souboru v adresáři uživatele (user home).${NORMAL}
${BOLD}send${NORMAL} [jméno] ${CYAN}# odešle soubor daného jména na server (jen testování). Pokud jméno není platný soubor, tak příkaz zobrazuje adresář.${NORMAL}
 ${BOLD}${YELLOW}Start interaktivního zadávání parametrů. Pro ukončení zadejte: ${NORMAL}${BOLD}!${NORMAL}[!!...] (jeden ${BOLD}!${NORMAL} pro každou podskupinu) (Hodnota může být seznam o max. velikosti %d položek.) (Hodnota může být libovolně velký seznam.) Aktuální config je Zdrojová odpověď Dostupné EPP příkazy Povolené hodnoty Soubor s certifikátem nebyl nalezen Jména certifikátů nejsou zadána  Certifikát chybí. Zkouším spojení bez SSL! Zdrojový příkaz Příkaz byl odeslán na EPP server. Potvrzení bylo nastaveno na Potvrzení je nastaveno na Připojen na host ${GREEN}${BOLD}%s${NORMAL}, port %d Spojení přerušeno Spojení uzavřeno Vytvoření defaultního config souboru selhalo. Defaultní config soubor byl uložen. Další informace naleznete v helpu. Výpis adresáře Chcete odeslat tento poříkaz na server? Dokument má chybné kódování. LookupError: %s EPP dokument není validní Příklad zadání Příklady Fatální chyba: Vytvoření defaultních config hodnot selhalo. Pro spojení s EPP serverem zadejte "connect" nebo rovnou "login". Pro deaktivaci validátoru zadejte Pro více informací zadejte "help" (nebo "h", "?") Pro více informací zadejte Interaktivní zadávání parametrů se přeruší zadáním "!" (nebo vícevykřičníků najednou, když jste v podskupině parametrů) Přišla Greeting zpráva Help pro příkaz IP adresa Jestliže tento skript běží v MS Windows a timeout není nula, tak se pravděpodobně jedná o SSL bug! Nastavte timeout zpět na nulu. Není možné vytvořit spojení. Požadované hodnoty z config chybí Není možné uložit config soubor. Důvod Aktivováno SSL spojení Místo "příkaz" vyberte jeden z následujícího seznamu: Interní chyba: Nadřazený uzel '%s' neexistuje. Přeložená odpověď Přeložený příkaz Přerušeno uživatelem Neplatný XML dokument. ExpatError: %s Nesprávné použití závorek (childs). Nesprávné použití závorek (list). Nesprávné použití závorek (mode). Neplatný vstupní formát Neplatný index parametru Neplatný kód odpovědi Seznam DNS Načíst soubor Login se nezdařil V odpovědi chybí část result Chybí parametry. Požadované minimum je Žádný config Žádná data Žádná odpověď. EPP server neodpovídá. Nenalezen Parametr MUSÍ být hodnota z následujícího seznamu Privátní klíč nebyl nalezen Odeslán logout Odpověď serveru není validní! Nastavený jazyk relace je Jazyk relace byl nastaven na Relace zahájena! Aktuální nastavení validace je Dočasný soubor pro ověření XML EPP validity se nepodařilo vytvořit. Důvod EPP příkaz "delete" se používá pro odebrání instance vybraného objektu. EPP příkazem "hello" si lze kdykoliv vyžádat od serveru odpověď "greeting". EPP příkaz "logout" se používá pro ukončení spojení s EPP serverem. EPP příkaz "poll" se používá k odběru servisních zpráv pro přihlášeného uživatele a ke zjištění počtu těchto zpráv uložených ve frontě. EPP příkaz "renew" se používá pro prodloužení platnosti vybraného objektu. EPP příkaz "update" se používá pro aktualizaci hodnot instance vybraného objektu. Server není správně nakonfigurován. Obraťte se na správce serveru. Tento kód jazyka není povolen Interaktivní režim zadávání parametrů příkazu se spustí: ${BOLD}!příkaz${NORMAL} Zkuste Zadejte Více informací o parametrech příkazu získáte zadáním "?příkaz" (nebo "h(elp) příkaz"). Neznámý EPP příkaz. Vyberte jeden ze seznamu EPP příkazů (zadejte help). Neznámý EPP příkaz: %s. Neznámý příkaz Neznámý kód jazyka Neznámé jméno parametru Neznámý typ části response Odpověď serveru nebyla rozpoznána Použití Použití: python ccreg_console.py [host] [lang] # (lang může být pouze cs/en a může být zadán před host) Použitý certifikát není podepsán uznávanou certifikační autoritou. DPH Validace byla nastavena na Validátor byl deaktivován. Opětná aktivace se provede zadáním Hodnota "%s" není povolena. Platná je: Vítejte v ccReg konzoli Jste již zalogován Nejste připojeni! Po připojení zadejte: connect nebo login Nejste připojeni! Pro připojení k serveru zadejte login. Nejste připojeni. Nejste zalogováni. Před samotnou prací na serveru musíte volat funkci login() povoleny pouze hodnoty část add adresa část change město kontakt kontakt ID jméno kontaktu kód země aktuální datum expirace veřejná adresa veřejný email veřejný fax indikátor zveřejnění veřejné jméno veřejný název organizace část pro veřejnost veřejný telefon jméno domény fax index zprávy, povinné při op=ack! seznam DNS Počet položek v seznamu je překročen. Maximum je seznam o maximálně %d položkách. chybí jméno nové heslo oznámení na email nsset adresa jméno nssetu počet měsíců nebo roků nepovinný název organizace heslo období jednotka období (y rok(default), m měsíc) poll ack je PSČ poštovní informace typ požadavku readline modul chybí - historie příkazů je deaktivována vlastník domény část remove povinný č.p. ulice tech. kontakt technický kontakt libovolně velký seznam telefon město vaše kontaktní ID váš email vaše login jméno vaše jméno vaše heslo 