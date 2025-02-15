<?php

namespace App;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class AttackModel
{
    public string $added;
    public string $country;
    public string $date;
    public string $domain;
    public string $summary;
    public string $title;
    public string $url;
    public string $victim;
    public ?VictimModel $victim_data;

    public function __construct(array $data)
    {
        $this->added = $data['added'] ?? '';
        $this->country = $data['country'] ?? '';
        $this->date = $data['date'] ?? '';
        $this->domain = $data['domain'] ?? '';
        $this->summary = $data['summary'] ?? '';
        $this->title = $data['title'] ?? '';
        $this->url = $data['url'] ?? '';
        $this->victim = $data['victim'] ?? '';
        $this->victim_data = isset($data['victim_data']) ? new VictimModel($data['victim_data']) : null;
    }
}