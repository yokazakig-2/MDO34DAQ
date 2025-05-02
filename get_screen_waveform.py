import pyvisa
import time

# VISAリソースマネージャの初期化
rm = pyvisa.ResourceManager()

# 接続するオシロのアドレス（適宜変更してください）
scope = rm.open_resource('USB0::0x0699::0x052C::C020606::INSTR')  # 実機アドレスに置き換える

# タイムアウト延長（ミリ秒）
scope.timeout = 20000

# 必要に応じてID確認
print(scope.query("*IDN?"))

#data points
record_length = 100000

#Record length
scope.write("HORizontal:RECOrdlength {}".format(record_length))

#Horizontal Scale 
scope.write(":HORizontal:SCAle 100E-6")

#Trigger
scope.write(":TRIGger:A:MODe NORMal")
scope.write(":TRIGger:A:EDGE:SOURce CH1")
scope.write(":TRIGger:A:EDGE:SLOPe RISe")
scope.write(":TRIGger:A:LEVel:CH1 -0.4")


# 波形取得対象のチャンネル（CH1など）
scope.write(":DATa:SOUrce CH1")
scope.write(":DATa:START 1")
scope.write(":DATa:STOP {}".format(record_length))
print("set CH1")

# データ形式：ASCII（読みやすく保存用）
scope.write(":WFMOutpre:ENCdg ASCii")
scope.write(":WFMOutpre:BYT_Nr 2")
scope.write(":WFMOutpre:NR_Pt {}".format(record_length))
scope.write(":HEADer 0")

print("set ASCii")

scope.write(":ACQuire:STATE RUN")
scope.write(":ACQuire:STOPAfter SEQuence")

# 波形データを取得
# データをファイルに保存
for i in range(3):
    osc_status = scope.query(":ACQuire:STATE?")

    while "1" in osc_status:
        if "1" in osc_status: print("Wait for trigger signals")
        time.sleep(1)
        osc_status = scope.query(":ACQuire:STATE?")

    print("Read data")

    data = scope.query(":CURVE?")
    with open("waveform_screen.csv", "a") as f:
        f.write(data)
        f.close()
    scope.write(":ACQuire:STATE RUN")


print("波形データを取得して waveform_screen.csv に保存しました。")
