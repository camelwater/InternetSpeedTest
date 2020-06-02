######### Absolute monitoring values ########## 
$maxpacketloss              = 2     #how much % packetloss until we alert. 
$MinimumDownloadSpeed       = 5    #What is the minimum expected download speed in Mbit/ps
$MinimumUploadSpeed         = 2     #What is the minimum expected upload speed in Mbit/ps

#need change to the path on your computer
$FilePath                = 'C:\internet\InternetSpeedTest.csv'    
######### End absolute monitoring values ######
 
#Replace the Download URL to where you've uploaded the ZIP file yourself. We will only download this file once. 
#Latest version can be found at: https://www.speedtest.net/apps/cli
$DownloadURL                = "https://bintray.com/ookla/download/download_file?file_path=ookla-speedtest-1.0.0-win64.zip"
$DownloadLocation           = "C:\internet\SpeedtestCLI"

$lines = Get-Content $FilePath | Measure-Object -Line
$2lines = (Select-String -Path "InternetSpeedTest.csv" -Pattern "RyanNetwork_2.4" -AllMatches).Matches.Count
$5lines = (Select-String -Path "InternetSpeedTest.csv" -Pattern "RyanNetwork_5GHz" -AllMatches).Matches.Count
$GEXTlines = (Select-String -Path "InternetSpeedTest.csv" -Pattern "RyanNetwork_5GHz_5GEXT" -AllMatches).Matches.Count
'''
if($lines.Lines > 100)
{
    
    if($2lines+100 == $5lines || $2lines+100 == $GEXTlines)
    {
        netsh wlan connect name=RyanNetwork
    }
    
    else if($5lines+100 == $2lines || $5lines+100 == $GEXTlines)
    {
        netsh wlan connect name=RyanNetwork_5GHz
    }
    else if($GEXTlines+100 == $5lines || $GEXTlines+100 == $2lines)
    {
        netsh wlan connect name=RyanNetwork_5GHz_5GEXT
    }
}

Start-Sleep -s 7
'''

try {
    $TestDownloadLocation   = Test-Path $DownloadLocation
    if (!$TestDownloadLocation) 
    {
        new-item $DownloadLocation -ItemType Directory -force
        Invoke-WebRequest -Uri $DownloadURL -OutFile "$($DownloadLocation)/speedtest.zip"
        Expand-Archive "$($DownloadLocation)/speedtest.zip" -DestinationPath $DownloadLocation -Force
    }
}
catch {  
    write-host "The download and extraction of SpeedtestCLI failed. Error: $($_.Exception.Message)"
    exit 1
}

$PreviousResults            = if (test-path "$($DownloadLocation)/LastResults.txt") { get-content "$($DownloadLocation)/LastResults.txt" | ConvertFrom-Json }
$SpeedtestResults           = & "$($DownloadLocation)/speedtest.exe" --format=json --accept-license --accept-gdpr --server-id=10142
$SpeedtestResults | Out-File "$($DownloadLocation)/LastResults.txt" -Force
$SpeedtestResults           = $SpeedtestResults | ConvertFrom-Json
 
#creating object
[PSCustomObject]$SpeedtestObj = @{
    downloadspeed = [math]::Round($SpeedtestResults.download.bandwidth / 1000000 * 8, 2)
    uploadspeed   = [math]::Round($SpeedtestResults.upload.bandwidth / 1000000 * 8, 2)
    packetloss    = [math]::Round($SpeedtestResults.packetLoss)
    isp           = $SpeedtestResults.isp
    ExternalIP    = $SpeedtestResults.interface.externalIp
    InternalIP    = $SpeedtestResults.interface.internalIp
    UsedServer    = $SpeedtestResults.server.host
    ResultsURL    = $SpeedtestResults.result.url
    Jitter        = [math]::Round($SpeedtestResults.ping.jitter)
    Latency       = [math]::Round($SpeedtestResults.ping.latency)
    ssid          = (get-netconnectionProfile).Name
}
if($SpeedtestResults -Match "error:")
{
    write-host ""
    write-host "error, couldn't get info"

    $SpeedtestObj.downloadspeed = -1
    $SpeedtestObj.uploadspeed = -1
    $SpeedtestObj.packetloss = -1
}
else
{
    write-host ""
    write-host "download speed: " $SpeedtestObj.downloadspeed ", upload speed: " $SpeedtestObj.uploadspeed ", ping: " $SpeedtestObj.Latency

    $SpeedtestHealth = @()
    #Comparing against previous result. Alerting is download or upload differs more than 20%.
    if ($PreviousResults) 
    {
        if ($PreviousResults.download.bandwidth / $SpeedtestResults.download.bandwidth * 100 -le 80) 
        { 
          $SpeedtestHealth += "Download speed difference is more than 20%" 
        }
        if ($PreviousResults.upload.bandwidth / $SpeedtestResults.upload.bandwidth * 100 -le 80) 
        { 
            $SpeedtestHealth += "Upload speed difference is more than 20%" 
        }
    }
 
    #Comparing against preset variables.
    if ($SpeedtestObj.downloadspeed -lt $MinimumDownloadSpeed) 
    { 
        $SpeedtestHealth += "Download speed is lower than $MinimumDownloadSpeed Mbit/ps" 
    }
    if ($SpeedtestObj.uploadspeed -lt $MinimumUploadSpeed) 
    { 
        $SpeedtestHealth += "Upload speed is lower than $MinimumUploadSpeed Mbit/ps" 
    }
    if ($SpeedtestObj.packetloss -gt $MaxPacketLoss) 
    { 
        $SpeedtestHealth += "Packetloss is higher than $maxpacketloss%" 
    }
    if(!$SpeedtestHealth)
    {
        $SpeedtestHealth = "its fine"
    }
    write-host ""
    write-host "Speed Test Results: " $SpeedtestHealth

}
$CurrentDateTime = (Get-Date -Format "dddd MM/dd/yyyy HH:mm" | Out-String).Trim()
$comma = ','
$dl = $SpeedtestObj.downloadspeed
$ul = $SpeedtestObj.uploadspeed
$pl = $SpeedtestObj.packetloss 

$id = $SpeedtestObj.ssid

if($id == "RyanNetwork")
{
    $id = "RyanNetwork_2.4"
}
$OutputString = $CurrentDateTime + $comma + $dl + $comma + $ul + $comma + $pl + $comma + $id
write-host ""
write-host "output: " $OutputString
#write-host "SSID: " $id
$OutputString | Out-File -FilePath $FilePath -Encoding utf8 -Append 