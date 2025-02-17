<?php

use Livewire\Volt\Component;
use App\APIService;

new class extends Component {

    public $attacks;
    public $attacksRes;
    public $errorMessage;
    public $countryCode = "ZA";

    public function mount()
    {
        $apiService = new APIService();
        $this->attacksRes = $apiService->getAttacks($this->countryCode);

        // dd($this->attacksRes);
        // if (gettype($this->attacksRes) === null) {
        if (count($this->attacksRes) === 0) {
            $this->errorMessage = "Oops! Your Country (" . $this->countryCode . ") could not be found. 404";
            return;
        }
        $this->attacks = $this->attacksRes['attacks'];
        // dump($this->attacks[0]);
        // dd($this->attacks);
    }
}; ?>

<!-- Attack Cards Feed Section -->
<section class="w-full flex justify-center items-center gap-5 flex-col">
    @if (!$errorMessage)
        {{-- Statistics Card --}}
        <div class=" bg-gray-900 w-full text-gray-100 p-5 md:p-6 rounded-lg shadow-lg relative overflow-hidden">
            <!-- Futuristic background element -->
            <div
                class="absolute top-0 right-0 w-32 h-32 bg-yellow-500 opacity-10 transform rotate-45 translate-x-16 -translate-y-16">
            </div>

            <!-- Impact stats -->
            <div class="grid grid-cols-3 gap-4 mb-4">
                <div class="bg-gray-800 p-3 rounded-lg">
                    <p class="text-xs text-gray-400 font-mono">Total People Affected</p>
                    <p class="text-xl font-bold text-yellow-400 font-mono">
                        {{ $attacksRes['total_affected_people']}}
                    </p>
                </div>
                <div class="bg-gray-800 p-3 rounded-lg">
                    <p class="text-xs text-gray-400 font-mono">Total Affected Customers</p>
                    <p class="text-xl font-bold text-yellow-400 font-mono">
                        {{ $attacksRes['total_affected_customers']}}
                    </p>
                </div>
                <div class="bg-gray-800 p-3 rounded-lg">
                    <p class="text-xs text-gray-400 font-mono">Total Affected Employees</p>
                    <p class="text-xl font-bold text-yellow-400 font-mono">
                        {{ $attacksRes['total_affected_employees']}}
                    </p>
                </div>
                <div class="bg-gray-800 p-3 rounded-lg">
                    <p class="text-xs text-gray-400 font-mono">Total 3rd Party Affected</p>
                    <p class="text-xl font-bold text-yellow-400 font-mono">
                        {{ $attacksRes['total_affected_third_parties']}}
                    </p>
                </div>
            </div>

            <!-- Futuristic footer element -->
            <div class="h-1 w-full bg-gradient-to-r from-yellow-500 to-yellow-200 rounded-full"></div>
        </div>
    @endif


    <h2 class="text-2xl w-full text-start font-bold text-yellow-400 mb-4">Recent Cyber Attacks</h2>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-5 w-full">
        @if($errorMessage)
            <h3 class="text-xl font-bold text-center text-red-400 mb-4">{{ $errorMessage }}</h2>
        @endif


            {{-- Map Attacks --}}
            @foreach($attacks as $attack)
                <div class=" bg-gray-900 w-full text-gray-100 p-5 md:p-6 rounded-lg shadow-lg relative overflow-hidden">
                    <!-- Futuristic background element -->
                    <div
                        class="absolute top-0 right-0 w-32 h-32 bg-yellow-500 opacity-10 transform rotate-45 translate-x-16 -translate-y-16">
                    </div>

                    <!-- Company and timestamp -->
                    <div class="w-full flex justify-center items-center flex-col gap-3 mb-6">
                        <div class="flex justify-between items-center w-full">
                            @if($attack['country'] === 'ZA' || $attack['country'] === 'ZAF')
                                <x-flag-4x3-za class="w-8" />
                            @endif
                            @if($attack['country'] === 'NA' || $attack['country'] === 'NA')
                                <x-flag-4x3-na class="w-8" />
                            @endif
                            <span class="text-sm text-gray-400 font-mono">{{ $attack['date'] }}</span>
                        </div>
                        <h2 class="w-full text-2xl md:text-start font-bold text-yellow-400 underline font-mono">
                            <a class="w-full" target="_blank" href="http://{{ $attack['domain'] }}">
                                {{ $attack['victim'] }}
                            </a>
                        </h2>
                    </div>

                    <!-- Attack details -->
                    <div class=" space-y-3 mb-6">
                        <p class="font-mono flex justify-start items-center flex-col md:flex-row">
                            <span class="text-yellow-400">News Source: </span>
                        <div class="flex justify-start items-center flex-wrap w-full gap-3">
                            {{ $attack['title'] }}
                            <a class="" target="_blank" href="{{ $attack['article_url'] }}">
                                {{ svg('feathericon-link', 'w-5') }}
                            </a>
                        </div>
                        </p>
                        <p class="font-mono">
                            <span class="text-yellow-400">Hacker Group:</span>
                            <span class="ml-2 text-lg">{{ $attack['hacker_group'] }}</span>
                        </p>
                        {{-- <p class="font-mono">
                            <span class="text-yellow-400">Compromised Data:</span>
                            <span class="ml-2">{{ $attack['compromised_data'] }}</span>
                        </p> --}}
                    </div>

                    <!-- Impact stats -->
                    <div class="grid grid-cols-3 gap-4 mb-4">
                        @if ($attack['affected']['customers'] !== 0)
                            <div class="bg-gray-800 p-3 rounded-lg">
                                <p class="text-xs text-gray-400 font-mono">Affected Customers</p>
                                <p class="text-xl font-bold text-yellow-400 font-mono">
                                    {{ $attack['affected']['customers'] }}
                                </p>
                            </div>
                        @endif
                        @if ($attack['affected']['employees'] !== 0)
                            <div class="bg-gray-800 p-3 rounded-lg">
                                <p class="text-xs text-gray-400 font-mono">Affected Employees</p>
                                <p class="text-xl font-bold text-yellow-400 font-mono">
                                    {{ $attack['affected']['employees'] }}
                                </p>
                            </div>
                        @endif
                        @if ($attack['affected']['third_parties'] !== 0)
                            <div class="bg-gray-800 p-3 rounded-lg">
                                <p class="text-xs text-gray-400 font-mono">3rd Party Affected</p>
                                <p class="text-xl font-bold text-yellow-400 font-mono">
                                    {{ $attack['affected']['third_parties'] }}
                                </p>
                            </div>
                        @endif
                    </div>

                    <!-- Futuristic footer element -->
                    <div class="h-1 w-full bg-gradient-to-r from-yellow-500 to-yellow-200 rounded-full"></div>
                </div>
            @endforeach
    </div>
</section>