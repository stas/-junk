<?php
class Result implements Polynom {
    public $polynom;
    
    function _read(){
        die( "Result can't be read.\n" );
    }
    
    function _print(){
        echo $this->polynom->toString() . "\n";
    }
}
?>