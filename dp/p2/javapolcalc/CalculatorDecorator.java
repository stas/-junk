/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

/**
 * Decorator for CalculatorEngine class
 * @author stas
 */
abstract public class CalculatorDecorator implements CalculatorEngine {
    public CalculatorDecorator(){
        this.printOperators();
    }

    public void printOperators() {
        System.out.println( "Resulted operators:" );
        System.out.println( divident.polynom.toString() );
        System.out.println( divider.polynom.toString() );
    }
}
