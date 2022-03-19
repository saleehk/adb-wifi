const mDnsSd = require('node-dns-sd');
const { exec } = require("child_process");
const shelljs = require('shelljs')

var qrcode = require('qrcode-terminal');
const { nanoid } = require('nanoid');
const name = 'ADB_WIFI_'+nanoid()
const password = nanoid()
function showQR() {
    
    const text = `WIFI:T:ADB;S:${name};P:${password};;`
    qrcode.generate(text, { small: true })
}
// showQR();
function getDevice(service) {
    return {
        address: service.address,
        port: service.service.port
    }


}
function connect({address,port}) {
    exec(`adb pair ${address}:${port} ${password}`, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });
}
async function startDiscover() {
    const device_list = await mDnsSd.discover({
        name: '_adb-tls-pairing._tcp.local'
    });
    if (device_list.length === 0)
        return await startDiscover();
    const item = getDevice(device_list[0])
    connect(item)


}
function main() {
    console.log("[Developer options]->[Wireless debugging]->[Pair device with QR code]");
    showQR();
    startDiscover();

}
main();
