/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javapolcalc;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Divident class that uses Polynom interface
 * @author stas
 */
public final class Divident implements Polynom {
    Polynomial polynom;

    public Divident(){
        this.read();
    }

    public void read() {
        InputStreamReader conv = new InputStreamReader(System.in);
        BufferedReader in = new BufferedReader(conv);

        // Start a new null polynomial
        Polynomial p = new Polynomial(0, 0);

        // Temporary coefficient and degree
        int tempC; int tempD;
        String[] tempS;

        System.out.println("Please type the divident polynom:");
        String s = null;
        try {
            s = in.readLine();
        } catch (IOException ex) {
            Logger.getLogger(Divider.class.getName()).log(Level.SEVERE, null, ex);
        }

        // Explode all the terms
        String[] newS = s.split("\\+");
            // Parse all the terms
            for( int i = 0; i < newS.length; i++) {
                // Split the coefficients and the degree
                tempS = newS[i].split("x\\^");
                    // Get the coefficient and the degree
                    tempC = Integer.valueOf(tempS[0]);
                    tempD = Integer.valueOf(tempS[1]);
                    // Add values to our polynomial
                    Polynomial tmp = new Polynomial(tempC, tempD);
                    p = p.plus(tmp);
            }
        
        this.polynom = p;
    }

    public void print() {
        System.out.println(this.polynom.toString());
    }

}
