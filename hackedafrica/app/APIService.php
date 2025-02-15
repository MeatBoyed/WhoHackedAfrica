<?php

namespace App;

use Http;
use Log;
use Illuminate\Http\Client\RequestException;
use Illuminate\Http\Response;
use App\AttackModel;
use App\VictimModel;

class APIService
{
    private $baseUrl = "https://api.ransomware.live/v2";

    public function getAttacks(string $countryCode): array
    {
        $url = "$this->baseUrl/countrycyberattacks/$countryCode";

        try {
            $response = Http::get($url); // Fetch the Attacks in region

            if ($response->successful()) {
                $attacks = $response->json();
                // $attacks = json_decode($response->get(), true);

                // Enrich each attack with victim details
                // $attackObjects = [];
                // foreach ($attacks as $attack) {
                //     $victimData = $this->getVictimData($attack['victim']);
                //     Log::Info("Collected Victim data - " . $victimData . "" . $attack);

                //     $attack['victim_data'] = $victimData;
                //     // $attackObjects[] = new AttackModel($attack);
                // }

                Log::Info("Collected & Formatted Attack Data");
                return $attacks;
            }
        } catch (\Exception $e) {
            Log::error("Error fetching cyber attacks: " . $e->getMessage());
        }

        return [];
    }

    private function getVictimData(string $domain): array
    {
        $url = "$this->baseUrl/victims/";

        try {
            $response = Http::get($url . $domain);
            $victim = $response->json();
            $err = $victim['error'] === null ? false : true;

            if ($err) {
                Log::error('Victim not found: ' . $victim);
                return [];
            }

            return $victim;
        } catch (\Exception $e) {
            Log::error("Error fetching victim data for $domain: " . $e->getMessage());
        }

        return [];
    }
}


// class APIService
// {

//     public string $base_url = "https://api.ransomware.live/v2/";
//     public string $rssfeed_url = "https://ransomware.live/rss.xml";

//     /**
//      * Create a new class instance.
//      */
//     public function __construct()
//     {
//         //
//     }

//     // Get list of Attackes (Filer by Country)
//     /**
//      * Summary of getAttacks
//      * @param string $countryCode
//      */
//     public function getAttacks(string $countryCode)
//     {
//         //  Make Request
//         $endpoint = $this->base_url . "countrycyberattacks/" . $countryCode;
//         $response = Http::get($endpoint);

//         // Handle Response
//         // Determine if the status code is >= 400...
//         if ($response->clientError()) {
//             $error = $response->json();
//             dump($error);
//             return 'Client Side error occured';
//         }

//         // $response->throwIfClientError(function (RequestException $err) {
//         //     dump($err);
//         // });

//         // Store Res Data as Objects
//         // $data = json_decode($response->getBody(), true);
//         $data = json_decode($response->getBody(), true);

//         // // Get Victims
//         // foreach ($data as $key => $attack) {
//         //     $name = $attack['victim'];
//         //     $attack['victim'] = $this->getVictim($name);
//         // }

//         // Return
//         return $data;
//     }

//     public function getVictim(string $name)
//     {
//         // Make Request
//         $endpoint = $this->base_url . "searchvictims/" . $name;
//         $response = Http::get($endpoint);
//         $victim = json_decode($response->getBody(), true);

//         // dump($victim);
//         $res = $victim["error"] ?? null;

//         if ($res !== null) {
//             return $name;
//         }

//         return $victim;
//     }
// }