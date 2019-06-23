package mocom.musician.util;

import org.springframework.stereotype.Service;

import java.io.*;

@Service(value = "OperateFile")
public class OperateFile {
    public String readFile(String path) {
        String string = "";
        try (FileReader reader = new FileReader(path);
             BufferedReader br = new BufferedReader(reader) // 建立一个对象，它把文件内容转成计算机能读懂的语言
        ) {
            String line;
            //网友推荐更加简洁的写法
            while ((line = br.readLine()) != null) {
                // 一次读入一行数据
                System.out.println(line);
                string += line;
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return string;
    }

    /**
     * 写入TXT文件
     */
    public void writeFile(String path, String string) {
        try {
            File writeName = new File(path); // 相对路径，如果没有则要建立一个新的output.txt文件
            writeName.createNewFile(); // 创建新文件,有同名的文件的话直接覆盖
            try (BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(writeName), "UTF-8"))) {
                out.write(string);
                out.flush(); // 把缓存区内容压入文件
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
