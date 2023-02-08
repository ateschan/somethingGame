import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) throws Exception {
        Scanner scan = new Scanner(System.in);
        
        String[] arr = new String[8];

    

        for(int i = 0; i < 8; i++){
            arr[i] = scan.nextLine();
            
            
        }
        
        
        int e = scan.nextInt();
        while (e!=0){
            int input = scan.nextInt();
            
                for(int i = 0; i < 8; i++){
                    String[] str = arr[i].split(" ", 2);
                    int num = Integer.parseInt(str[1]);
                    
                        if ((input < 535) || (input > 1605)){
                            System.out.println("BAD INPUT");
                            i = 8;
                        }
                    int count2 = 0;
                        for(int g = 0; g < (str[0]).length(); g++) {    
                            if((str[0]).charAt(g) != ' ')    
                                count2++;    
                                }
                    if (count2 > 4){
                        
                        System.out.println("BAD INPUT");
                            i = 8;
                    }
                }
            e--;
        }
        
    }
}