import zipfile
import xml.etree.ElementTree as ET
import os

class UDFParser:
    """
    UDFParser sınıfı, UDF dosyasının içeriğini işlemek için kullanılır.

    Parametreler:
    - udfPath (str): UDF dosyasının yolu

    Kullanım:
    - UDFParser sınıfını oluştururken 'udfPath' parametresi verilmelidir.
    - getContent metodu, UDF içeriğini döndürür.

    Örnek:
    udfParser = UDFParser(udfPath="test.udf")
    udfData = udfParser.getContent()
    print(udfData)
    """

    def __init__(self, udfPath=""):
        """
        UDFParser sınıfının başlatıcı metodudur.

        Parametreler:
        - udfPath (str): UDF dosyasının yolu

        İşlev:
        - UDF dosya yolu geçerliliği ve formatı kontrol edilir.
        """
        if udfPath == "":
            raise ValueError("UDF path is empty")

        if not udfPath.endswith(".udf"):
            raise ValueError("UDF path is not a .udf file")

        if not os.path.exists(udfPath):
            raise FileNotFoundError("UDF path does not exist")

        if not zipfile.is_zipfile(udfPath):
            raise ValueError("UDF path is not a valid .udf file")

        self.udfPath = udfPath

    def readUdf(self):
        """
        UDF içeriğini okuyan metod.

        İşlev:
        - UDF dosyasından content.xml çıkarılır ve içeriği okunur.
        - XML ağacı oluşturulur ve kök düğüm döndürülür.
        """
        with zipfile.ZipFile(self.udfPath, 'r') as udfContent:
            udfContent.extract("content.xml")

        dataTree = ET.parse("content.xml")
        dataRoot = dataTree.getroot()

        if os.path.exists("content.xml"):
            os.remove("content.xml")

        return dataRoot

    def getContent(self):
        """
        UDF içeriğini döndüren metod.

        İşlev:
        - readUdf metodunu kullanarak XML içeriğini elde eder.
        - <content> etiketlerini görmezden gelerek içeriği döndürür.
        """
        try:
            data = self.readUdf()
            udfContent = data.find(".//content")
            if udfContent is not None and udfContent.text is not None:
                return udfContent.text.strip()
            else:
                return "No content found"
        except Exception as e:
            raise Exception("UDF content not found")
