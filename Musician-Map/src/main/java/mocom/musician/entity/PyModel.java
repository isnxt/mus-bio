package mocom.musician.entity;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class PyModel {
    public void analyse(String pyPath, String inPath, String outPath) {
        System.out.println(inPath + " " + outPath);
        String command = pyPath + "\\venv\\Scripts\\python.exe " + pyPath + "\\py2java.py" + " " + inPath + " " + outPath;
        System.out.println(command);
        String line = null;
        StringBuilder sb = new StringBuilder();
        Runtime runtime = Runtime.getRuntime();
        try {
            Process process=runtime.exec(command);
                        BufferedReader bufferedReader = new BufferedReader
                    (new InputStreamReader(process.getInputStream()));
            while ((line = bufferedReader.readLine()) != null) {
                System.out.println(line);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println("python end");

    }
}
