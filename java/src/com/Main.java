package com;
import java.io.*;

public class Main {

    public static void main(String[] args) {
        // 调用python部分需要指定的路径
        String pyPath = "E:\\Musician-Bio\\NLP-zh";  // python 工程路径
        String inPath = "E:\\Musician-Bio\\JDemo\\in.txt"; // 待处理的文本txt路径
        String outPath = "E:\\Musician-Bio\\JDemo\\out.txt"; // 已处理的文本txt路径

        PyModel pyModel = new PyModel();
        pyModel.anaylse(pyPath,inPath,outPath);

        /*
         * out.txt 格式)
         * 第1行：第1句话的时间列表，以‘|’分隔
         * 第2行：第1句话的人物列表，以‘|’分隔
         * 第3行：第1句话的地点列表，以‘|’分隔
         * 第4行：第1句话的事情列表，以‘|’分隔
         * 第5行：第2句话的时间列表，以‘|’分隔
         * 第6行：第2句话的人物列表，以‘|’分隔
         * 第7行：第2句话的地点列表，以‘|’分隔
         * 第8行：第2句话的事情列表，以‘|’分隔
         * ...
         */
        try {
            BufferedReader in = new BufferedReader(new FileReader(outPath));
            String str;
            while ((str = in.readLine()) != null) {
                System.out.println(str);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
