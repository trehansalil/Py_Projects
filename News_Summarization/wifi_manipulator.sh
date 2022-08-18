# if nmcli radio wifi is enabled then nothing else run nmcli radio wifi on

alpha=$(nmcli radio wifi)

echo "$alpha"

if [ "$alpha" = "disabled" ]; then
  nmcli radio wifi on
  echo "Enabling your Wifi connection"
fi