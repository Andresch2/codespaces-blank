grammar gramatica;

// ======= Reglas de alto nivel =======
// Un programa es una secuencia de sentencias
program      : statement+ EOF ;

// Una sentencia puede ser asignación, regla "si", o print
statement    : assignment
             | ruleStmt
             | printStmt
             ;

// Asignación:  ID = expr ;
assignment   : ID '=' expr ';' ;

// Regla: si <condición>: <acción>   (una sola acción, como en el enunciado)
ruleStmt     : SI cond ':' action ;

// Acción interna de la regla: ID = expr ;
action       : ID '=' expr ';' ;

// Condición:  ID <op> expr
cond         : ID comparator expr ;

// print(ID);
printStmt    : PRINT '(' ID ')' ';' ;

// ======= Expresiones aritméticas =======
// + y - en nivel expr; * y / en nivel term; paréntesis en factor
expr         : expr ('+'|'-') term
             | term
             ;

term         : term ('*'|'/') factor
             | factor
             ;

factor       : NUMBER
             | ID
             | '(' expr ')'
             ;

// Comparadores (según consigna)
comparator   : '<' | '>' | '>=' | '<=' ;

// ======= Tokens =======
SI           : 'si' ;
PRINT        : 'print' ;

NUMBER       : [0-9]+ ('.' [0-9]+)? ;
ID           : [a-zA-Z_][a-zA-Z_0-9]* ;

COMMENT      : '//' ~[\r\n]* -> skip ;
WS           : [ \t\r\n]+ -> skip ;
