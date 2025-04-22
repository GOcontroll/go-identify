#!/usr/bin/env python3
import subprocess
import threading
from argparse import ArgumentParser, BooleanOptionalAction

def led_flashing():
    try:
        subprocess.run(["go-flash-leds", "-r", "500", "5"], capture_output=True)
    except:
        pass

def get_module_name(module: str) -> str:
    if "20-10-1" in module:
        return "6 channel input"
    elif "20-10-2" in module:
        return "10 channel input"
    elif "20-10-3" in module:
        return "4 - 20mA input"
    elif "20-20-1" in module:
        return "2 channel power bridge"
    elif "20-20-2" in module:
        return "6 channel output"
    elif "20-20-2" in module:
        return "10 channel output"
    elif "20-30-3" in module:
        return "IR communication"
    else:
        return None

def identify():
    parser = ArgumentParser(
        prog="identify",
        description="""identify\n
        Print some information about the controller and flash leds if present""",
        add_help=True,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        action=BooleanOptionalAction,
        default=False,
        help="print more information"
    )
    parser.add_argument(
        "-s",
        "--scan-modules",
        required=False,
        action=BooleanOptionalAction,
        default=False,
        help="actively scan for modules (interrupts simulink/nodered)"
    )
    args = parser.parse_args()

    tf = threading.Thread(target=led_flashing)
    tf.start()

    print("Software/Hardware info:")
    os = subprocess.run(["lsb_release", "-ds"], capture_output=True)
    print(f"OS: {os.stdout.decode('utf-8').strip()}")
    kernel = subprocess.run(["uname", "-r"], capture_output=True)
    print(f"Kernel: {kernel.stdout.decode('utf-8').strip()}")
    model = subprocess.run(["cat", "/sys/firmware/devicetree/base/model"], capture_output=True)
    print(f"Model: {model.stdout.decode('utf-8')}")
    hardware = subprocess.run(["cat", "/sys/firmware/devicetree/base/hardware"], capture_output=True)
    print(f"Hardware: {hardware.stdout.decode('utf-8').strip()}\n")
    #print("\nSerial Number:")
    #subprocess.run(["go-sn", "r"])

    if args.scan_modules:
        try:
            subprocess.run(["go-modules", "scan"], capture_output=True)
        except:
            print("could not run `go-modules scan`")

    print("Module configuration: ")
    try:
        with open("/usr/lib/gocontroll/modules", "r") as modulesfile:
            layout = modulesfile.readline()[:-1]
            manufacturers = modulesfile.readline()[:-1]
            moduleQRsfront = modulesfile.readline()[:-1]
            moduleQRsback = modulesfile.readline()
    except:
        print("no module configuration found, run `go-modules scan` first")
        return

    modules = layout.split(":")
    manufacturers = manufacturers.split(":")
    moduleQRsfront = moduleQRsfront.split(":")
    moduleQRsback = moduleQRsback.split(":")

    if args.verbose:
        output=[["Slot", "Type", "HW Version", "SW Version", "Manufacturer", "QR front", "QR back"]]   
        for i,module in enumerate(modules):
            toAppend = [f"{i+1}"]
            name = get_module_name(module)
            if name == None:
                toAppend = toAppend + ["-", "-", "-", "-", "-", "-"]
                output.append(toAppend)
            else: 
                toAppend.append(name)
                moduleSplit = module.split("-")
                toAppend = toAppend + [moduleSplit[3], moduleSplit[4]+"."+moduleSplit[5]+"."+moduleSplit[6], manufacturers[i], moduleQRsfront[i], moduleQRsback[i]]
                output.append(toAppend)
    else:
        output=[["Slot", "Type", "HW Version", "SW Version"]]   
        for i,module in enumerate(modules):
            toAppend = [f"{i+1}"]
            name = get_module_name(module)
            if name == None:
                toAppend = toAppend + ["-", "-", "-"]
                output.append(toAppend)
            else:
                toAppend.append(name)
                moduleSplit = module.split("-")
                toAppend = toAppend + [moduleSplit[3], moduleSplit[4]+"."+moduleSplit[5]+"."+moduleSplit[6]]
                output.append(toAppend)

    s = [[str(e) for e in row] for row in output]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))
    tf.join()

if __name__ == "__main__":
    identify()
