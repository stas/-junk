/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

/**
 * Interface Class for Calculator
 * @author stas
 */
public interface CalculatorEngine {
    // Facade for our Operators
    Divident divident = new Divident();
    Divider divider = new Divider();
    
    public void printOperators();
 }
