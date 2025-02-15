<?php

namespace App;

class VictimModel
{
    public string $activity;
    public string $attackdate;
    public string $claim_url;
    public string $country;
    public string $description;
    public string $discovered;
    public string $domain;
    public string $group;
    public array $infostealer;
    public ?string $press;
    public string $screenshot;
    public string $url;
    public string $victim;

    public function __construct(array $data)
    {
        $this->activity = $data['activity'] ?? '';
        $this->attackdate = $data['attackdate'] ?? '';
        $this->claim_url = $data['claim_url'] ?? '';
        $this->country = $data['country'] ?? '';
        $this->description = $data['description'] ?? '';
        $this->discovered = $data['discovered'] ?? '';
        $this->domain = $data['domain'] ?? '';
        $this->group = $data['group'] ?? '';
        $this->infostealer = $data['infostealer'] ?? [];
        $this->press = $data['press'] ?? null;
        $this->screenshot = $data['screenshot'] ?? '';
        $this->url = $data['url'] ?? '';
        $this->victim = $data['victim'] ?? '';
    }
}