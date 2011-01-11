<?php
include "Polynom.class.php";
include "Polynomial.class.php";

class Divident implements Polynom {
    public $polynom;
    
    function Divident() {
        $this->_read();
        $this->_print();
    }
    
    function _read(){
        $this->polynom = new Polynomial(0, 0);
        echo "Please type in the divident:\n";
        
        $f = fopen('php://stdin', 'r');
        $line = fgets($f);
        
        $members = explode( "+", $line );
        for( $i = 0; $i < count( $members ); $i++ ) {
            $m = explode( "x^", $members[$i] );
            $tmp_p = new Polynomial( $m[0], $m[1] );
            $this->polynom = $this->polynom->plus( $tmp_p );
        }
    }
    
    function _print(){
        echo $this->polynom->toString() . "\n";
    }
}
?>