import pyvisa
import time
import argparse
import sys

parser = argparse.ArgumentParser(
    prog="argparse_check",
    usage="python check.py -ne <nevents> -np <npoints> -hs <hscale> -dt <delay> -rf <first> -rl <last> -tch <tchannel> -thr <threshold> -rch <rchannel> -dw <dwidth> -of <filename> --fall",
    description="check waveform",
    epilog="",
    add_help=True,
)

parser.add_argument("-ne",  "--nevents",   type=int,   default=10000,                 help="Set number of events")
parser.add_argument("-np",  "--npoints",   type=int,   default=100000,                help="Set sampling points : 1000, 10000, 100000, 1000000, 5000000, 10000000")
parser.add_argument("-hs",  "--hscale",    type=float, default=100E-6,                help="Set horizontal scale [s/div], full time range is horizontal scale * 10")
parser.add_argument("-dt",  "--delay",     type=float, default=50,                    help="Set the trigger timing on a display [%]")
parser.add_argument("-rf",  "--first",     type=int,   default=1,                     help="Record first point")
parser.add_argument("-rl",  "--last",      type=int,   default=100000,                help="Record last point")
parser.add_argument("-tch", "--tchannel",  type=int,   default=1,                     help="Trigger Channel")
parser.add_argument("-thr", "--threshold", type=float, default=-0.4,                  help="Set threshold [V]")
parser.add_argument("-rch", "--rchannel",  type=int,   default=1,                     help="Record Channel")
parser.add_argument("-dw",  "--dwidth",    type=int,   default=1,                     help="The number of bytes per data point")
parser.add_argument("-of",  "--filename",  type=str,   default="waveform_screen.csv", help="Output file name")
parser.add_argument("--fall", action="store_true", help="Trigger type : falling")

args=parser.parse_args()

TSCH="CH"+str(args.tchannel)
RCH ="CH"+str(args.tchannel)

TType="RISe"
if args.fall:
    TType="FALL"


#Error check
if args.npoints not in [1000, 10000, 100000, 1000000, 5000000, 10000000]:
    print("You try to set wrong sampling points. Select in [1000, 10000, 100000, 1000000, 5000000, 10000000]")
    sys.exit()

if args.first > args.npoints:
    print("First Point : "+str(args.first)+", but Sampling points : "+str(args.npoints)+". You should set the first data point smaller than sampling points.")
    sys.exit()

if args.last > args.npoints:
    print("Last Point : "+str(args.last)+", but Sampling points : "+str(args.npoints)+". You should set the last data point smaller than sampling points.")
    sys.exit()

if args.first > args.last:
    print("First Point : "+str(args.first)+", but Last Point : "+str(args.last)+". You should set the last data point larger than the first data.")
    sys.exit()

if args.tchannel > 4 or args.tchannel < 1:
    print("You can select CH1-4 as a trigger source channel")
    sys.exit()

if args.rchannel > 4 or args.rchannel < 1:
    print("You can select CH1-4 as a record channel")
    sys.exit()

if args.dwidth < 1 or args.dwidth > 2:
    print("You can select only 1 or 2")
    sys.exit()

# VISAリソースマネージャの初期化
rm = pyvisa.ResourceManager()

# 接続するオシロのアドレス（適宜変更してください）
scope = rm.open_resource('USB0::0x0699::0x052C::C020606::INSTR')  # 実機アドレスに置き換える

# タイムアウト延長（ミリ秒）
scope.timeout = 20000

# 必要に応じてID確認
print(scope.query("*IDN?"))

#Record length
scope.write("HORizontal:RECOrdlength {}".format(args.npoints))

#Horizontal Scale 
scope.write(":HORizontal:SCAle {}".format(args.hscale))

#Delay time
scope.write(":HORizontal:POSition {}".format(args.delay))

#Trigger
scope.write(":TRIGger:A:MODe NORMal")
scope.write(":TRIGger:A:EDGE:SOURce {}".format(TSCH))
scope.write(":TRIGger:A:EDGE:SLOPe {}".format(TType))
scope.write(":TRIGger:A:LEVel:CH1 {}".format(args.threshold))


# 波形取得対象のチャンネル（CH1など）
scope.write(":DATa:SOUrce {}".format(RCH))
scope.write(":DATa:START {}".format(args.first))
scope.write(":DATa:STOP {}".format(args.last))
print("set CH1")

# データ形式：ASCII（読みやすく保存用）
scope.write(":WFMOutpre:ENCdg ASCii")
scope.write(":WFMOutpre:BYT_Nr {}".format(args.dwidth))
#scope.write(":WFMOutpre:NR_Pt {}".format(record_length))
scope.write(":HEADer 0")

print("set ASCii")

scope.write(":ACQuire:STATE RUN")
scope.write(":ACQuire:STOPAfter SEQuence")

start = time.time()

# 波形データを取得
# データをファイルに保存
for i in range(args.nevents):
    osc_status = scope.query(":ACQuire:STATE?")

    while "1" in osc_status:
        if "1" in osc_status: print("Wait for trigger signals")
        #time.sleep(1)
        osc_status = scope.query(":ACQuire:STATE?")

    print("Read data")

    data = scope.query(":CURVE?")
    with open("{}".format(args.filename), "a") as f:
        f.write(data)
        f.close()
    scope.write(":ACQuire:STATE RUN")

end = time.time()

print("波形データを取得して {} に保存しました。".format(args.filename))
print(f"実行時間: {end - start:.6f} 秒")
