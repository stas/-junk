<?php
include "Divident.class.php";
include "Divider.class.php";
include "Result.class.php";

class Calculator {
    public $divident;
    public $divider;
    public $result;
    
    function Calculator() {
        $this->divident = new Divident();
        $this->divider = new Divider();
        $this->result = new Result();
        
        $this->sum();
    }
    
    function sum() {
        $this->result->polynom = $this->divident->polynom->plus( $this->divider->polynom );
        $this->result->_print();
    }
    
    function getInstance() {
        static $instance;
        if( !is_object( $instance ) )
            $instance = new Calculator();
        
        return $instance;
    }
}
?>