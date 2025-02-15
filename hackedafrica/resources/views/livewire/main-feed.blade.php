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
        dump($this->attacks[0]);
    }
}; ?>

<!-- Attack Cards Feed Section -->
<section class="w-full">
    <h2 class="text-2xl font-bold text-yellow-400 mb-4">Recent Cyber Attacks</h2>

    <div class="grid grid-cols-1 gap-5 w-full">
        {{-- Map Attacks --}}
        @foreach($attacks as $attack)
            {{-- @livewire('attack-card', [
            'attack' => $attack
            ]) --}}
            {{-- <livewire:attack-card :attack= /> --}}

            <div class="bg-gray-900 w-full text-gray-100 p-5 md:p-6 rounded-lg shadow-lg relative overflow-hidden">
                <!-- Futuristic background element -->
                <div
                    class="absolute top-0 right-0 w-32 h-32 bg-yellow-500 opacity-10 transform rotate-45 translate-x-16 -translate-y-16">
                </div>

                <!-- Company and timestamp -->
                <div class="w-full flex justify-center items-center flex-col gap-3 mb-6">
                    <div class="flex justify-between items-center w-full">
                        <x-flag-4x3-za class="w-8" />
                        <span class="text-sm text-gray-400 font-mono">{{ $attack['date'] }}</span>
                    </div>
                    <a href=" https://{{ $attack['domain'] }}">
                        <h2 class=" text-2xl font-bold text-yellow-400 underline font-mono">{{ $attack['victim'] }}</h2>
                    </a>
                </div>

                <!-- Attack details -->
                <div class=" space-y-3 mb-6">
                    <p class="font-mono">
                        <span class="text-yellow-400">Hacker Group:</span>
                        {{-- <span class="ml-2 text-lg">{{ $attack['hacker_group'] }}</span> --}}
                    </p>
                    <p class="font-mono">
                        <span class="text-yellow-400">Compromised Data:</span>
                        {{-- <span class="ml-2">{{ $attack['compromised_data'] }}</span> --}}
                    </p>
                </div>

                <!-- Impact stats -->
                <div class="grid grid-cols-3 gap-4 mb-4">
                    <div class="bg-gray-800 p-3 rounded-lg">
                        <p class="text-xs text-gray-400 font-mono">Affected Customers</p>
                        {{-- <p class="text-xl font-bold text-yellow-400 font-mono">{{ $attack['affected_customers'] }}
                        </p>
                        --}}
                    </div>
                    <div class="bg-gray-800 p-3 rounded-lg">
                        <p class="text-xs text-gray-400 font-mono">Affected Employees</p>
                        {{-- <p class="text-xl font-bold text-yellow-400 font-mono">{{ $attack['affected_employees'] }}
                        </p>
                        --}}
                    </div>
                    <div class="bg-gray-800 p-3 rounded-lg">
                        <p class="text-xs text-gray-400 font-mono">3rd Party Affected</p>
                        {{-- <p class="text-xl font-bold text-yellow-400 font-mono">{{ $attack['third_party_affected']
                            }}
                        </p> --}}
                    </div>
                </div>

                <!-- Futuristic footer element -->
                <div class="h-1 w-full bg-gradient-to-r from-yellow-500 to-yellow-200 rounded-full"></div>
            </div>
        @endforeach
    </div>
</section>