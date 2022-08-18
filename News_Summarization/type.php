<?php
$output = shell_exec('ps -ef | grep python');
echo "<pre>$output</pre>";
?>

<!-- <?php

use Salil\WiFi\WiFi;

class Example
{
    public $device;

    /**
     * @throws Exception
     */
    public function getAllNetworks()
    {
        $allNetworks = WiFi::scan()->getAll();

        if (count($allNetworks) > 0) {
            foreach ($allNetworks as $network) {
                echo $network . "\n";
            }
        }
    }

    /**
     * @param $ssid
     * @param $password
     * @throws Exception
     */
    public function connect($ssid, $password)
    {
        $networks = WiFi::scan()
            ->getBySsid($ssid);

        if (count($networks) > 0) {
            $networks[0]->connect($password, $this->device);
        } else {
            echo "Network $ssid wasn't found!\r\n";
        }
    }

    /**
     * @throws Exception
     */
    public function disconnect()
    {
        $connectedNetworks = WiFi::scan()->getConnected();

        foreach ($connectedNetworks as $network) {
            $network->disconnect($this->device);
        }
    }
}

$example = new Example();
try {
    $example->device = 'en1';
    $example->getAllNetworks();
    $example->connect('Salil', 'thanos$468A!');
    $example->disconnect();
} catch (Exception $e) {
    //
}
?> -->