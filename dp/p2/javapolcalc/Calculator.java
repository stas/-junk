/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Calculator class based on CalculatorDecorator
 * @author stas
 */
public final class Calculator extends CalculatorDecorator {
    // Facade for our Result Operator
    Result result = new Result();
    
    public Calculator( ) {
        sum();
    }

    @Override
    public void printOperators() {
        
    }

    public void sum() {
        this.result.polynom = this.divident.polynom.plus(this.divider.polynom);
        this.result.print();
        try {
            this.result.saveLog();
        } catch (IOException ex) {
            Logger.getLogger(Calculator.class.getName()).log(Level.SEVERE, null, ex);
        }
    }
}
