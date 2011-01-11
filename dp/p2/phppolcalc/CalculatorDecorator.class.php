<?php
include "Divident.class.php";
include "Divider.class.php";
include "Result.class.php";
include "CalculatorEngine.class.php";

/**
 * Decorator for CalculatorEngine class
 */
abstract class CalculatorDecorator implements CalculatorEngine {
    // Facades for our operators
    public $divident;
    public $divider;
    
    function __constructor() {
        $this->divident = new Divident();
        $this->divider = new Divider();
        
        $this->printOperators();
    }
    
    function printOperators(){
        echo "Resulted operators:\n";
        $this->divident->_print();
        $this->divider->_print();
    }
}
?>