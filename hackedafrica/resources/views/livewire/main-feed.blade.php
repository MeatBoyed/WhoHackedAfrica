<?php

use Livewire\Volt\Component;
use App\APIService;

new class extends Component {

    public $attacks;

    public function mount()
    {
        $apiService = new APIService();

        $this->attacks = $apiService->getAttacks("ZA");
        // $this->updatedAttacks = $apiService->getVictim($this->attacks);
        dump($this->attacks);
    }
}; ?>

<!-- Attack Cards Feed Section -->
<section>
    <h2 class="text-2xl font-bold text-yellow-400 mb-4">Recent Cyber Attacks</h2>

    <div class="space-y-6">
        {{-- Map Attacks --}}
        @foreach($attacks as $attack)
            @livewire('attack-card', [
                'attack' => $attack
            ])
        @endforeach
    </div>
</section>