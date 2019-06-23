package com;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

/*
 * Description: 用来连接Python Model的示例
 */

public class PyModel {

    public void anaylse(String pyPath,String inPath,String outPath) {
        String command= pyPath + "\\venv\\Scripts\\python.exe"+" "+ pyPath+"\\py2java.py"+" "+ inPath+" "+ outPath;
        String line = null;
        StringBuilder sb = new StringBuilder();
        Runtime runtime = Runtime.getRuntime();
        try {
            runtime.exec(command);

        } catch (IOException e) {
            // TODO 自动生成的 catch 块
            e.printStackTrace();
        }
    }
}
