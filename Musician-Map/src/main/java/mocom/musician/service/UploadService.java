package mocom.musician.service;

import mocom.musician.entity.PyModel;
import mocom.musician.util.BytesEncodingDetect;
import org.springframework.stereotype.Service;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Service(value = "UploadService")
public class UploadService {
    public List<String> mainPy(String pyPath, String inPath, String outPath) {
        PyModel pyModel = new PyModel();
        pyModel.analyse(pyPath, inPath, outPath);
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
        List<String> allLine = new ArrayList<>();
        File file = new File(outPath);
        while (!file.exists()) {
        }
        try {
            BufferedReader in = new BufferedReader(new FileReader(outPath));
            String str;
            while ((str = in.readLine()) != null) {
                allLine.add(str);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return allLine;
    }

    public boolean dectect(String inputFileUrl) {
        BytesEncodingDetect bytesEncodingDetect = new BytesEncodingDetect();
        String inputFileEncode = BytesEncodingDetect.javaname[bytesEncodingDetect.detectEncoding(new File(inputFileUrl))];
        if (inputFileEncode.equals("UTF-8")) {
            return false;
        }
        return true;
    }

    public void chageFormat(String inputFileUrl, String outputFileUrl) throws IOException {
        BytesEncodingDetect bytesEncodingDetect = new BytesEncodingDetect();
        String inputFileEncode = BytesEncodingDetect.javaname[bytesEncodingDetect.detectEncoding(new File(inputFileUrl))];
        System.out.println("inputFileEncode===" + inputFileEncode);
        BufferedReader bufferedReader = new BufferedReader(
                new InputStreamReader(new FileInputStream(inputFileUrl), inputFileEncode));
        BufferedWriter bufferedWriter = new BufferedWriter(
                new OutputStreamWriter(new FileOutputStream(outputFileUrl), "UTF-8"));
        String line;
        while ((line = bufferedReader.readLine()) != null) {
            bufferedWriter.write(line + "\r\n");
        }
        bufferedWriter.close();
        bufferedReader.close();
        String outputFileEncode = BytesEncodingDetect.javaname[bytesEncodingDetect.detectEncoding(new File(outputFileUrl))];
        System.out.println("outputFileEncode===" + outputFileEncode);
        System.out.println("txt文件格式转换完成");
    }
}
