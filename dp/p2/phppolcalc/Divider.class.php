<?php
class Divider implements Polynom {
    public $polynom;
    
    function Divider() {
        $this->_read();
        $this->_print();
    }
    
    function _read(){
        $this->polynom = new Polynomial(0, 0);
        echo "Please type in the divider:\n";
        
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