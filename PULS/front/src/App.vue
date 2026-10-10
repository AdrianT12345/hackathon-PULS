<template>
  <div class="app">

    <div class="age-modal-overlay" v-if="showAgeModal">
      <div class="age-modal">
        <div class="age-modal-header">
          <img class="logo_header" src="/images/logo.png" alt="logo">
        </div>
        <div class="age-modal-content">
          <p>
            Podaj swój wiek, aby dostosować wyświetlane wydarzenia do Twoich
            potrzeb.
          </p>
          <div class="age-input-group">
            <label for="userAgeInput">Twój wiek:</label>
            <input
              type="number"
              id="userAgeInput"
              v-model.number="userAge"
              min="1"
              max="120"
              placeholder="np. 25"
              @keyup.enter="confirmAge"
            />
          </div>
        </div>
        <div class="age-modal-footer">
          <button
            class="age-confirm-btn"
            @click="confirmAge"
            :disabled="!userAge || userAge < 1"
          >
            Potwierdź
          </button>
        </div>
      </div>
    </div>

    <div class="admin-modal-overlay" v-if="showAdminModal">
      <div class="admin-modal">
        <div class="admin-modal-header">
          <h2>Panel Admina</h2>
          <button class="close-modal-btn" @click="showAdminModal = false">✕</button>
        </div>
        <div class="admin-modal-content">
          <p>Wprowadź hasło administratora aby uzyskać dostęp do ukrytych treści.</p>
          <div class="admin-input-group">
            <label for="adminPassword">Hasło:</label>
            <input
              type="password"
              id="adminPassword"
              v-model="adminPassword"
              placeholder="Wprowadź hasło"
              @keyup.enter="loginAdmin"
            />
          </div>
          <div class="admin-error" v-if="adminError">{{ adminError }}</div>
        </div>
        <div class="admin-modal-footer">
          <button class="admin-login-btn" @click="loginAdmin" :disabled="!adminPassword">
            Zaloguj się
          </button>
        </div>
      </div>
    </div>


    <!-- Górny pasek nawigacji -->
    <header class="topbar">
      <div class="topbar-brand">
        <img class="logo" src="/images/logo.png" alt="logo">
      </div>
      
      <nav class="topbar-nav">
        <button
          :class="['nav-btn', { active: activeSection === 'demografia' }]"
          @click="toggleSection('demografia')"
        >
          Demografia
        </button>
        <button
          :class="['nav-btn', { active: activeSection === 'transport' }]"
          @click="toggleSection('transport')"
        >
          Transport
        </button>
        <button
          :class="['nav-btn', { active: activeSection === 'spolecznosc' }]"
          @click="toggleSection('spolecznosc')"
        >
          Społeczność
        </button>
        <button
          :class="['nav-btn', { active: activeSection === 'zdrowie' }]"
          @click="toggleSection('zdrowie')"
        >
          Miejsca
        </button>
      </nav>

      <div class="topbar-actions">
        <button 
          v-if="!isAdmin" 
          class="login-btn"
          @click="showAdminModal = true"
        >
          Zaloguj
        </button>
        <div class="admin-badge" v-if="isAdmin" @click="logoutAdmin">
          ADMIN
        </div>
      </div>
      
      <!-- Hamburger menu dla mobile -->
      <button class="mobile-menu-btn" @click="mobileMenuOpen = !mobileMenuOpen">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </header>

    <!-- Mobile menu -->
    <div class="mobile-menu" v-if="mobileMenuOpen" @click="mobileMenuOpen = false">
      <button
        :class="['mobile-nav-btn', { active: activeSection === 'demografia' }]"
        @click="toggleSection('demografia')"
      >Demografia</button>
      <button
        :class="['mobile-nav-btn', { active: activeSection === 'transport' }]"
        @click="toggleSection('transport')"
      >Transport</button>
      <button
        :class="['mobile-nav-btn', { active: activeSection === 'spolecznosc' }]"
        @click="toggleSection('spolecznosc')"
      >Społeczność</button>
      <button
        :class="['mobile-nav-btn', { active: activeSection === 'zdrowie' }]"
        @click="toggleSection('zdrowie')"
      >Miejsca</button>
      <button 
        v-if="!isAdmin" 
        class="mobile-nav-btn"
        @click="showAdminModal = true"
      >Zaloguj</button>
    </div>


    <div class="main-content">
      <div id="map" class="map-container"></div>


      <div class="section-panel" v-if="activeSection === 'demografia'">
        <h3>Demografia</h3>
        <div class="section-content">
          <div class="filter-group">
            <span>Kategoria:</span>
            <div class="filter-buttons">
              <button
                v-for="cat in categories"
                :key="cat.id"
                :class="['filter-btn', { active: activeCategory === cat.id }]"
                @click="selectCategory(cat.id)"
              >
                {{ cat.name }}
              </button>
            </div>
          </div>
          <div class="filter-group">
            <span>Płeć:</span>
            <div class="filter-buttons">
              <button
                v-for="demo in demographyOptions"
                :key="demo.id"
                :class="[
                  'filter-btn',
                  { active: selectedDemography === demo.id },
                ]"
                @click="selectDemography(demo.id)"
              >
                {{ demo.name }}
              </button>
            </div>
          </div>
          <div class="filter-group">
            <span>Wiek:</span>
            <div class="filter-buttons">
              <button
                v-for="age in ageOptions"
                :key="age.id"
                :class="['filter-btn', { active: selectedAge === age.id }]"
                @click="selectAge(age.id)"
              >
                {{ age.name }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="section-panel" v-if="activeSection === 'spolecznosc'">
        <h3>Społeczność</h3>
        <div class="section-content">
          <div class="filter-group">
            <span>Filtry:</span>
            <div class="filter-buttons">
              <button
                :class="['filter-btn', { active: spolecznoscFilter === 'all' }]"
                @click="spolecznoscFilter = 'all'"
              >
                Wszystkie
              </button>
              <button
                :class="[
                  'filter-btn',
                  { active: spolecznoscFilter === 'zgloszenie' },
                ]"
                @click="spolecznoscFilter = 'zgloszenie'"
              >
                Zgłoszenia
              </button>
              <button
                :class="[
                  'filter-btn',
                  { active: spolecznoscFilter === 'wydarzenie' },
                ]"
                @click="spolecznoscFilter = 'wydarzenie'"
              >
                Wydarzenia
              </button>
            </div>
          </div>
          <div class="filter-group">
            <span>Widok:</span>
            <div class="filter-buttons">
              <button
                :class="['filter-btn heatmap-btn', { active: heatmapEnabled }]"
                @click="toggleHeatmap"
              >
                Heat mapa {{ heatmapEnabled ? "ON" : "OFF" }}
              </button>
            </div>
          </div>
        </div>
      </div>


      <div v-if="activeSection === 'demografia'">
        <div class="info-panel" v-if="hoveredDzielnica">
          <h3>{{ hoveredDzielnica.nazwa }}</h3>
          <p>
            <strong>{{ currentDemographyLabel }}:</strong>
            {{ formatNumber(getPopulationByDemography(hoveredDzielnica)) }}
          </p>
          <p>
            <strong>Gęstość:</strong>
            {{ calculateDensityByDemography(hoveredDzielnica).toFixed(2) }}
            os/km²
          </p>
          <p>
            <strong>Powierzchnia:</strong>
            {{ hoveredDzielnica.powierzchnia.toFixed(2) }} km²
          </p>
          <hr />
          <p>
            <strong>Kobiety:</strong>
            {{ formatNumber(hoveredDzielnica.liczba_kobiet) }}
          </p>
          <p>
            <strong>Mężczyźni:</strong>
            {{ formatNumber(hoveredDzielnica.liczba_mezczyzn) }}
          </p>
          <hr />
          <p>
            <strong>Młodzi:</strong>
            {{
              formatNumber(
                (hoveredDzielnica.kobiety_mlodzi || 0) +
                  (hoveredDzielnica.mezczyzni_mlodzi || 0)
              )
            }}
          </p>
          <p>
            <strong>Dorośli:</strong>
            {{
              formatNumber(
                (hoveredDzielnica.kobiety_dorosli || 0) +
                  (hoveredDzielnica.mezczyzni_dorosli || 0)
              )
            }}
          </p>
          <p>
            <strong>Seniorzy:</strong>
            {{
              formatNumber(
                (hoveredDzielnica.kobiety_seniorzy || 0) +
                  (hoveredDzielnica.mezczyzni_seniorzy || 0)
              )
            }}
          </p>
        </div>
        <div class="info-panel info-hint" v-else>
          <p>Najedź na dzielnicę</p>
        </div>
      </div>

      <div v-if="activeSection === 'spolecznosc'">
        <div class="info-panel form-panel">
          <h3>Dodaj nowe zdarzenie</h3>
          <form @submit.prevent="submitZdarzenie" class="zdarzenie-form">
            <div class="form-group">
              <label>Lokalizacja:</label>
              <div
                class="location-display"
                v-if="noweZdarzenie.lokalizacja_lat && noweZdarzenie.dzielnica"
              >
                {{ noweZdarzenie.lokalizacja_lat.toFixed(5) }},
                {{ noweZdarzenie.lokalizacja_lng.toFixed(5) }}
                <br />
                <strong>Dzielnica:</strong> {{ noweZdarzenie.dzielnica }}
              </div>
              <div
                class="location-error"
                v-else-if="
                  noweZdarzenie.lokalizacja_lat && !noweZdarzenie.dzielnica
                "
              >
                ⚠️ Lokalizacja poza obszarem Gdańska!
                <br />
                <small>Wybierz punkt w obrębie dzielnicy.</small>
              </div>
              <div class="location-hint" v-else>
                Kliknij na mapę aby wybrać lokalizację
              </div>
            </div>

            <div class="form-group">
              <label>Typ zdarzenia:</label>
              <select
                v-model="noweZdarzenie.kategoria2"
                @change="noweZdarzenie.kategoria3 = ''"
                required
              >
                <option value="">-- Wybierz --</option>
                <option value="zgloszenie">Zgłoszenie</option>
                <option value="wydarzenie">Wydarzenie</option>
              </select>
            </div>

            <div class="form-group" v-if="noweZdarzenie.kategoria2">
              <label>Kategoria:</label>
              <select v-model="noweZdarzenie.kategoria3" required>
                <option value="">-- Wybierz kategorię --</option>
                <option
                  v-for="kat in dostepneKategorie"
                  :key="kat.id"
                  :value="kat.id"
                >
                  {{ kat.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Tytuł:</label>
              <input
                type="text"
                v-model="noweZdarzenie.tytul"
                required
                placeholder="Tytuł zdarzenia"
              />
            </div>

            <div class="form-group">
              <label>Opis:</label>
              <textarea
                v-model="noweZdarzenie.opis"
                required
                placeholder="Opis zdarzenia"
                rows="3"
              ></textarea>
            </div>

            <div class="form-group">
              <label>Termin od:</label>
              <input type="datetime-local" v-model="noweZdarzenie.termin_od" />
            </div>

            <div class="form-group">
              <label>Termin do:</label>
              <input type="datetime-local" v-model="noweZdarzenie.termin_do" />
            </div>

            <div class="form-group">
              <label>Minimalny wiek uczestnika:</label>
              <input
                type="number"
                v-model.number="noweZdarzenie.min_wiek"
                min="0"
                max="120"
                placeholder="0 = dla wszystkich"
              />
            </div>

            <div
              class="form-group checkbox-group"
              v-if="noweZdarzenie.kategoria2 === 'wydarzenie'"
            >
              <label class="checkbox-label">
                <input
                  type="checkbox"
                  v-model="noweZdarzenie.dla_niepelnosprawnych"
                />
                <span class="checkbox-text"
                  >♿ Dostosowane dla niepełnosprawnych</span
                >
              </label>
            </div>

            <button
              type="submit"
              class="submit-btn"
              :disabled="
                !noweZdarzenie.lokalizacja_lat || !noweZdarzenie.dzielnica
              "
            >
              Dodaj zdarzenie
            </button>

            <div class="form-message" v-if="formMessage">{{ formMessage }}</div>
          </form>
        </div>

        <!-- Panel generowania propozycji dla admina -->
        <div class="info-panel proposal-panel" v-if="isAdmin">
          <h3>🎯 Propozycje działań</h3>
          <p class="proposal-description">
            Generowanie propozycji na podstawie danych z mapy
          </p>
          <button 
            class="generate-btn" 
            @click="generateProposals"
            :disabled="generatingProposals"
          >
            {{ generatingProposals ? '⏳ Analizuję...' : '🔍 Analizuj dane i generuj propozycje' }}
          </button>
          
          <div class="proposals-list" v-if="proposals.length > 0">
            <div 
              class="proposal-item" 
              v-for="(proposal, index) in proposals" 
              :key="index"
              :class="proposal.type"
            >
              <div class="proposal-header">
                <span class="proposal-icon">{{ proposal.icon }}</span>
                <span class="proposal-type-badge" :class="proposal.type">{{ proposal.typeLabel }}</span>
              </div>
              <h4 class="proposal-title">{{ proposal.title }}</h4>
              <p class="proposal-desc">{{ proposal.description }}</p>
              <div class="proposal-meta">
                <span class="proposal-location">📍 {{ proposal.dzielnica }}</span>
                <span class="proposal-priority" :class="proposal.priority">
                  {{ proposal.priorityLabel }}
                </span>
              </div>
            </div>
          </div>
          
          <div class="proposals-empty" v-else-if="proposalsGenerated">
            <p>Brak propozycji do wygenerowania. Dodaj więcej zdarzeń na mapę.</p>
          </div>
        </div>

        <div class="dzielnice-ranking-panel">
          <h4>Aktywność mieszkańców</h4>
          <div class="ranking-filters">
            <button
              :class="[
                'ranking-filter-btn',
                { active: rankingSort === 'total' },
              ]"
              @click="rankingSort = 'total'"
            >
              Wszystko
            </button>
            <button
              :class="[
                'ranking-filter-btn',
                { active: rankingSort === 'zgloszenia' },
              ]"
              @click="rankingSort = 'zgloszenia'"
            >
              Zgłoszenia
            </button>
            <button
              :class="[
                'ranking-filter-btn',
                { active: rankingSort === 'wydarzenia' },
              ]"
              @click="rankingSort = 'wydarzenia'"
            >
              Wydarzenia
            </button>
          </div>
          <div class="ranking-list">
            <div
              v-for="(item, index) in dzielnicaRanking"
              :key="item.nazwa"
              class="ranking-item"
              :class="{ 'has-events': item.count > 0 }"
              @click="zoomToDzielnica(item.nazwa)"
              @mouseenter="highlightDzielnicaOnMap(item.nazwa)"
              @mouseleave="unhighlightDzielnicaOnMap()"
            >
              <span class="ranking-position">{{ index + 1 }}</span>
              <span class="ranking-name">{{ item.nazwa }}</span>
              <span class="ranking-count" :class="rankingSort">{{
                item.count
              }}</span>
            </div>
          </div>
        </div>


        <div class="dzielnica-stats-panel" v-if="hoveredDzielnicaSpolecznosc">
          <h4>📊 {{ hoveredDzielnicaSpolecznosc }}</h4>
          <div class="stats-grid">
            <div class="stat-item stat-all" v-if="spolecznoscFilter === 'all'">
              <span class="stat-number">{{ dzielnicaStats.total }}</span>
              <span class="stat-label">Wszystkich zdarzeń</span>
            </div>
            <div
              class="stat-item stat-zgloszenie"
              v-if="
                spolecznoscFilter === 'all' ||
                spolecznoscFilter === 'zgloszenie'
              "
            >
              <span class="stat-number">{{ dzielnicaStats.zgloszenia }}</span>
              <span class="stat-label">Zgłoszeń</span>
            </div>
            <div
              class="stat-item stat-wydarzenie"
              v-if="
                spolecznoscFilter === 'all' ||
                spolecznoscFilter === 'wydarzenie'
              "
            >
              <span class="stat-number">{{ dzielnicaStats.wydarzenia }}</span>
              <span class="stat-label">Wydarzeń</span>
            </div>
          </div>
        </div>
        <div class="dzielnica-stats-panel stats-hint" v-else>
          <p>Najedź na dzielnicę aby zobaczyć statystyki</p>
        </div>


        <div class="komentarze-panel" v-if="selectedZdarzenie">
          <div class="komentarze-header">
            <h4>💬 Komentarze</h4>
            <button class="close-btn" @click="closeKomentarzePanel">✕</button>
          </div>
          <div class="komentarze-zdarzenie-info">
            <strong>{{ selectedZdarzenie.tytul }}</strong>
            <span class="zdarzenie-type" :class="selectedZdarzenie.kategoria2">
              {{
                selectedZdarzenie.kategoria2 === "zgloszenie"
                  ? "🔴 Zgłoszenie"
                  : "🟢 Wydarzenie"
              }}
            </span>
          </div>

          <div class="komentarze-list" v-if="komentarze.length > 0">
            <div class="komentarz-item" v-for="kom in komentarze" :key="kom.id">
              <div class="komentarz-header">
                <span class="komentarz-autor">{{ kom.autor }}</span>
                <span class="komentarz-data">{{
                  formatKomentarzDate(kom.data_utworzenia)
                }}</span>
              </div>
              <p class="komentarz-tresc">{{ kom.tresc }}</p>
            </div>
          </div>
          <div class="komentarze-empty" v-else>
            <p>Brak komentarzy. Bądź pierwszy!</p>
          </div>

          <div class="komentarz-form">
            <input
              type="text"
              v-model="nowyKomentarz.autor"
              placeholder="Twoje imię (opcjonalne)"
              class="komentarz-input autor-input"
            />
            <textarea
              v-model="nowyKomentarz.tresc"
              placeholder="Napisz komentarz..."
              rows="2"
              class="komentarz-input tresc-input"
            ></textarea>
            <button
              class="submit-komentarz-btn"
              @click="submitKomentarz"
              :disabled="!nowyKomentarz.tresc.trim()"
            >
              Wyślij
            </button>
          </div>
        </div>
      </div>

      <div v-if="activeSection === 'transport'">
        <div class="info-panel">
          <h3>Ostatnia aktualizacja</h3>
          <p><strong></strong> {{ get_last_upadate_time() }}</p>
        </div>
      </div>


      <div class="section-panel" v-if="activeSection === 'zdrowie'">
        <h3>Ważne miejsca</h3>
        <div class="section-content">
          <div class="filter-group">
            <span>Kategoria:</span>
            <div class="filter-buttons">
              <button
                :class="[
                  'filter-btn',
                  { active: wazneMiejscaFilter === 'all' },
                ]"
                @click="wazneMiejscaFilter = 'all'"
              >
                Wszystkie
              </button>
              <button
                :class="[
                  'filter-btn',
                  { active: wazneMiejscaFilter === 'szkoly' },
                ]"
                @click="wazneMiejscaFilter = 'szkoly'"
              >
                🎓 Szkoły
              </button>
              <button
                :class="[
                  'filter-btn',
                  { active: wazneMiejscaFilter === 'apteki' },
                ]"
                @click="wazneMiejscaFilter = 'apteki'"
              >
                💊 Apteki i Szpitale
              </button>
            </div>
          </div>
          <div class="filter-group">
            <span>Widok:</span>
            <div class="filter-buttons">
              <button
                :class="[
                  'filter-btn heatmap-btn',
                  { active: wazneMiejscaHeatmap },
                ]"
                @click="toggleWazneMiejscaHeatmap"
              >
                Heat mapa {{ wazneMiejscaHeatmap ? "ON" : "OFF" }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeSection === 'zdrowie'">
        <div class="dzielnice-ranking-panel">
          <h4>🔍 Ranking dzielnic</h4>
          <div class="ranking-filters">
            <button
              :class="[
                'ranking-filter-btn',
                { active: wazneMiejscaRankingSort === 'total' },
              ]"
              @click="wazneMiejscaRankingSort = 'total'"
            >
              Wszystko
            </button>
            <button
              :class="[
                'ranking-filter-btn',
                { active: wazneMiejscaRankingSort === 'szkoly' },
              ]"
              @click="wazneMiejscaRankingSort = 'szkoly'"
            >
              Szkoły
            </button>
            <button
              :class="[
                'ranking-filter-btn',
                { active: wazneMiejscaRankingSort === 'apteki' },
              ]"
              @click="wazneMiejscaRankingSort = 'apteki'"
            >
              Apteki
            </button>
          </div>
          <div class="ranking-list">
            <div
              v-for="(item, index) in wazneMiejscaRanking"
              :key="item.nazwa"
              class="ranking-item"
              :class="{ 'has-events': item.count > 0 }"
              @click="zoomToDzielnica(item.nazwa)"
              @mouseenter="highlightDzielnicaOnMap(item.nazwa)"
              @mouseleave="unhighlightDzielnicaOnMap()"
            >
              <span class="ranking-position">{{ index + 1 }}</span>
              <span class="ranking-name">{{ item.nazwa }}</span>
              <span class="ranking-count" :class="wazneMiejscaRankingSort">{{
                item.count
              }}</span>
            </div>
          </div>
        </div>

        <div class="dzielnica-stats-panel" v-if="hoveredDzielnicaWazneMiejsca">
          <h4>📊 {{ hoveredDzielnicaWazneMiejsca }}</h4>
          <div class="stats-grid">
            <div class="stat-item stat-all" v-if="wazneMiejscaFilter === 'all'">
              <span class="stat-number">{{ wazneMiejscaStats.total }}</span>
              <span class="stat-label">Wszystkich</span>
            </div>
            <div
              class="stat-item stat-szkoly"
              v-if="
                wazneMiejscaFilter === 'all' || wazneMiejscaFilter === 'szkoly'
              "
            >
              <span class="stat-number">{{ wazneMiejscaStats.szkoly }}</span>
              <span class="stat-label">Szkół</span>
            </div>
            <div
              class="stat-item stat-apteki"
              v-if="
                wazneMiejscaFilter === 'all' || wazneMiejscaFilter === 'apteki'
              "
            >
              <span class="stat-number">{{ wazneMiejscaStats.apteki }}</span>
              <span class="stat-label">Aptek</span>
            </div>
          </div>
        </div>
        <div class="dzielnica-stats-panel stats-hint" v-else>
          <p>Najedź na dzielnicę aby zobaczyć statystyki</p>
        </div>


        <div class="info-panel analysis-panel" v-if="isAdmin">
          <h3>📊 Analiza niedoborów</h3>
          <p class="analysis-description">
            Analiza pokrycia dzielnic szkołami i aptekami
          </p>
          <button 
            class="generate-btn" 
            @click="analyzeInfrastructure"
            :disabled="analyzingInfrastructure"
          >
            {{ analyzingInfrastructure ? '⏳ Analizuję...' : '🔍 Analizuj infrastrukturę' }}
          </button>
          
          <div class="analysis-results" v-if="infrastructureAnalysis.length > 0">
            <div 
              class="analysis-item" 
              v-for="(item, index) in infrastructureAnalysis" 
              :key="index"
              :class="[item.type, { 'extreme': item.severity === 'extreme' }]"
            >
              <div class="analysis-header">
                <span class="analysis-icon">{{ item.icon }}</span>
                <span class="analysis-dzielnica">{{ item.dzielnica }}</span>
                <span class="analysis-severity" :class="item.severity">{{ item.severityLabel }}</span>
              </div>
              <p class="analysis-desc">{{ item.description }}</p>
              <div class="analysis-stats">
                <span>👥 {{ item.mieszkancy.toLocaleString() }} mieszkańców</span>
                <span v-if="item.type === 'szkola'">🎓 {{ item.count }} szkół</span>
                <span v-if="item.type === 'apteka'">💊 {{ item.count }} aptek</span>
                <span class="ratio">📈 {{ item.ratio }}</span>
              </div>
              <button 
                class="simulate-btn" 
                @click="simulateNewPlace(item)"
              >
                ➕ Symuluj dodanie {{ item.type === 'szkola' ? 'szkoły' : 'apteki' }}
              </button>
            </div>
          </div>
          
          <div class="analysis-empty" v-else-if="analysisCompleted">
            <p>✅ Wszystkie dzielnice mają odpowiednią infrastrukturę!</p>
          </div>


          <div class="simulated-places" v-if="simulatedPlaces.length > 0">
            <h4>🗺️ Symulowane lokalizacje</h4>
            <div 
              class="simulated-item" 
              v-for="(place, index) in simulatedPlaces" 
              :key="index"
            >
              <span class="simulated-icon">{{ place.type === 'szkola' ? '🎓' : '💊' }}</span>
              <span class="simulated-name">{{ place.nazwa }}</span>
              <span class="simulated-location">{{ place.dzielnica }}</span>
              <button class="remove-simulated-btn" @click="removeSimulatedPlace(index)">✕</button>
            </div>
            <button class="clear-simulations-btn" @click="clearAllSimulations">
              🗑️ Usuń wszystkie symulacje
            </button>
          </div>
        </div>
      </div>


      <div class="legend" v-if="activeSection === 'demografia'">
        <h4>{{ legendTitle }}</h4>
        <div class="legend-item" v-for="item in legendItems" :key="item.label">
          <span class="legend-color" :style="{ background: item.color }"></span>
          <span class="legend-label">{{ item.label }}</span>
        </div>
      </div>


    </div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.heat";
import axios from "axios";
import { toRaw } from "vue";

const API_URL = "http://localhost:8000/api/dzielnice-geojson/";
const ZDARZENIA_API_URL = "http://localhost:8000/api/zdarzenia/";

export default {
  name: "App",
  data() {
    return {
      map: null,
      geojsonLayer: null,
      zdarzeniaLayer: null,
      transportLayer: null,
      locationMarker: null,
      activeSection: "demografia",
      activeCategory: null,
      selectedDemography: "all",
      selectedAge: "all",
      hoveredDzielnica: null,
      dzielnicaData: null,
      zdarzeniaData: null,
      transportData: null,
      routeLayer: null,

      spolecznoscFilter: "all",
      formMessage: "",
      noweZdarzenie: {
        lokalizacja_lat: null,
        lokalizacja_lng: null,
        dzielnica: null,
        kategoria2: "",
        kategoria3: "",
        tytul: "",
        opis: "",
        termin_od: "",
        termin_do: "",
        min_wiek: 0,
        dla_niepelnosprawnych: false,
      },
      userAge: null,
      showAgeModal: true,
      dzielnicaBackgroundLayer: null,
      hoveredDzielnicaSpolecznosc: null,
      rankingSort: "total",
      highlightedDzielnicaLayer: null,
      heatmapEnabled: false,
      heatmapLayer: null,

      wazneMiejscaFilter: "all",
      wazneMiejscaHeatmap: false,
      wazneMiejscaHeatmapLayer: null,
      wazneMiejscaLayer: null,
      wazneMiejscaBackgroundLayer: null,
      wazneMiejscaRankingSort: "total",
      hoveredDzielnicaWazneMiejsca: null,
      szkolyData: [],
      aptekiData: [],

      selectedZdarzenie: null,
      komentarze: [],
      nowyKomentarz: {
        autor: "",
        tresc: "",
      },


      isAdmin: false,
      showAdminModal: false,
      adminPassword: "",
      adminError: "",
      mobileMenuOpen: false,
 
      proposals: [],
      proposalsGenerated: false,
      generatingProposals: false,
      

      infrastructureAnalysis: [],
      analysisCompleted: false,
      analyzingInfrastructure: false,
      simulatedPlaces: [],
      simulatedMarkersLayer: null,

      zgloszenieKategorie: [
        {
          id: "roboty_drogowe",
          name: "Roboty drogowe",
          icon: "under-construction.png",
        },
        {
          id: "wypadek_drogowy",
          name: "Wypadek na drodze",
          icon: "car-collision.png",
        },
        {
          id: "wypadek_ludzki",
          name: "Wypadek ludzki",
          icon: "injury.png",
        },
        { id: "korek", name: "Korek", icon: "traffic-jam.png" },
        { id: "pozar", name: "Pożar", icon: "fire.png" },
        { id: "zagrozenie", name: "Zagrożenie", icon: "dangere.png" },
        {
          id: "zle_parkowanie",
          name: "Złe parkowanie",
          icon: "no-parking.png",
        },
        { id: "bezdomny", name: "Bezdomny", icon: "poverty.png" },
        { id: "wandalizm", name: "Wandalizm", icon: "vandalism.png" },
      ],

      wydarzenieKategorie: [
        { id: "sportowe", name: "Wydarzenie sportowe", icon: "sport.png" },
        {
          id: "hobbystyczne",
          name: "Wydarzenie hobbystyczne",
          icon: "creative.png",
        },
        {
          id: "dla_dzieci",
          name: "Wydarzenie dla dzieci",
          icon: "children.png",
        },
        {
          id: "akcja_spoleczna",
          name: "Akcja społeczna",
          icon: "social-support.png",
        },
        {
          id: "kulturowe",
          name: "Wydarzenie kulturowe",
          icon: "culture.png",
        },
        {
          id: "religijne",
          name: "Wydarzenie religijne",
          icon: "religious.png",
        },
        { id: "muzyczne", name: "Wydarzenie muzyczne", icon: "concert.png" },
      ],
      categories: [
        { id: 1, name: "Mieszkańcy" },
        { id: 2, name: "Gęstość" },
        { id: 3, name: "Powierzchnia" },
      ],
      demographyOptions: [
        { id: "all", name: "Wszyscy" },
        { id: "kobiety", name: "Kobiety" },
        { id: "mezczyzni", name: "Mężczyźni" },
      ],
      ageOptions: [
        { id: "all", name: "Wszyscy" },
        { id: "mlodzi", name: "Młodzi (0-17)" },
        { id: "dorosli", name: "Dorośli (18-59)" },
        { id: "seniorzy", name: "Seniorzy (60+)" },
      ],
      legendItems: [
        { color: "#08306b", label: "> 30 000" },
        { color: "#2171b5", label: "20 000 – 30 000" },
        { color: "#4292c6", label: "15 000 – 20 000" },
        { color: "#6baed6", label: "10 000 – 15 000" },
        { color: "#9ecae1", label: "5 000 – 10 000" },
        { color: "#c6dbef", label: "1 000 – 5 000" },
        { color: "#deebf7", label: "< 1 000" },
      ],
    };
  },
  mounted() {
    this.$nextTick(() => {
      this.initMap();
      this.loadDzielnice();
      if (localStorage.getItem("isAdmin") === "true") {
        this.isAdmin = true;
      }
    });
  },
  methods: {
    initMap() {
      this.map = L.map("map").setView([54.372, 18.638], 11);


      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: "&copy; OpenStreetMap contributors",
        maxZoom: 19,
      }).addTo(toRaw(this.map));
    },

    confirmAge() {
      if (this.userAge && this.userAge >= 1) {
        this.showAgeModal = false;

        if (this.activeSection === "spolecznosc") {
          this.displayZdarzenia();
        }
      }
    },

    skipAge() {
      this.userAge = null;
      this.showAgeModal = false;
    },

    async loginAdmin() {
      if (!this.adminPassword) return;
      
      try {
        const response = await axios.post("http://localhost:8000/api/admin-login/", {
          password: this.adminPassword
        });
        
        if (response.data.success) {
          this.isAdmin = true;
          this.showAdminModal = false;
          this.adminPassword = "";
          this.adminError = "";

          localStorage.setItem("isAdmin", "true");
        }
      } catch (err) {
        this.adminError = "Nieprawidłowe hasło!";
        this.adminPassword = "";
      }
    },

    logoutAdmin() {
      this.isAdmin = false;
      localStorage.removeItem("isAdmin");
      if (this.activeSection === "admin") {
        this.activeSection = "demografia";
        this.refreshMap();
      }
    },

    exportData() {
      const data = {
        zdarzenia: this.zdarzeniaData,
        dzielnice: this.dzielnicaData,
        szkoly: this.szkolyData,
        apteki: this.aptekiData,
        exportDate: new Date().toISOString()
      };
      
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `puls-export-${new Date().toISOString().split("T")[0]}.json`;
      a.click();
      URL.revokeObjectURL(url);
    },

    refreshAllData() {
      this.loadDzielnice();
      if (this.activeSection === "spolecznosc") {
        this.loadZdarzenia();
      } else if (this.activeSection === "zdrowie") {
        this.loadWazneMiejsca();
      }
    },

    generateProposals() {
      this.generatingProposals = true;
      this.proposals = [];
      

      setTimeout(() => {
        const newProposals = [];
        
        if (!this.zdarzeniaData || !this.dzielnicaData) {
          this.generatingProposals = false;
          this.proposalsGenerated = true;
          return;
        }

        const dzielnicaStats = {};
        this.dzielnicaData.features.forEach(f => {
          dzielnicaStats[f.properties.nazwa] = {
            nazwa: f.properties.nazwa,
            zgloszenia: 0,
            wydarzenia: 0,
            problemy: {},
            mieszkancy: f.properties.liczba_mieszkancow || 0
          };
        });
        

        this.zdarzeniaData.features.forEach(f => {
          const dz = f.properties.dzielnica;
          if (dz && dzielnicaStats[dz]) {
            if (f.properties.kategoria2 === 'zgloszenie') {
              dzielnicaStats[dz].zgloszenia++;
              const kat = f.properties.kategoria3;
              dzielnicaStats[dz].problemy[kat] = (dzielnicaStats[dz].problemy[kat] || 0) + 1;
            } else {
              dzielnicaStats[dz].wydarzenia++;
            }
          }
        });
        

        Object.values(dzielnicaStats).forEach(dz => {
          if (dz.zgloszenia >= 3) {
            newProposals.push({
              type: 'intervention',
              typeLabel: 'Interwencja',
              icon: '🚨',
              title: `Pilna interwencja w dzielnicy ${dz.nazwa}`,
              description: `Wykryto ${dz.zgloszenia} zgłoszeń problemów. Zalecana jest wizja lokalna i koordynacja działań naprawczych.`,
              dzielnica: dz.nazwa,
              priority: 'high',
              priorityLabel: '🔴 Wysoki priorytet'
            });
          }
          

          if (dz.wydarzenia < 2 && dz.mieszkancy > 5000) {
            newProposals.push({
              type: 'event',
              typeLabel: 'Wydarzenie',
              icon: '🎉',
              title: `Organizacja wydarzenia w ${dz.nazwa}`,
              description: `Dzielnica z ${dz.mieszkancy.toLocaleString()} mieszkańcami ma mało wydarzeń. Proponujemy organizację festynu lub pikniku sąsiedzkiego.`,
              dzielnica: dz.nazwa,
              priority: 'medium',
              priorityLabel: '🟡 Średni priorytet'
            });
          }
          

          if (dz.problemy['zle_parkowanie'] >= 2) {
            newProposals.push({
              type: 'investment',
              typeLabel: 'Inwestycja',
              icon: '🅿️',
              title: `Budowa parkingu w ${dz.nazwa}`,
              description: `Zgłoszono ${dz.problemy['zle_parkowanie']} problemów z parkowaniem. Rekomendowana inwestycja w infrastrukturę parkingową.`,
              dzielnica: dz.nazwa,
              priority: 'medium',
              priorityLabel: '🟡 Średni priorytet'
            });
          }

          if (dz.problemy['wandalizm'] >= 2) {
            newProposals.push({
              type: 'social',
              typeLabel: 'Akcja społeczna',
              icon: '🛡️',
              title: `Program bezpieczeństwa w ${dz.nazwa}`,
              description: `Wykryto ${dz.problemy['wandalizm']} przypadków wandalizmu. Proponujemy kampanię społeczną i zwiększenie patroli.`,
              dzielnica: dz.nazwa,
              priority: 'high',
              priorityLabel: '🔴 Wysoki priorytet'
            });
          }
          
          if (dz.problemy['bezdomny'] >= 1) {
            newProposals.push({
              type: 'social',
              typeLabel: 'Akcja społeczna',
              icon: '🏠',
              title: `Pomoc bezdomnym w ${dz.nazwa}`,
              description: `Zgłoszono obecność osób bezdomnych. Proponujemy koordynację z MOPS i organizację pomocy.`,
              dzielnica: dz.nazwa,
              priority: 'high',
              priorityLabel: '🔴 Wysoki priorytet'
            });
          }

          if (dz.problemy['roboty_drogowe'] >= 1) {
            newProposals.push({
              type: 'info',
              typeLabel: 'Informacja',
              icon: '🚧',
              title: `Monitorowanie robót w ${dz.nazwa}`,
              description: `Trwają roboty drogowe. Zalecane monitorowanie postępu prac i informowanie mieszkańców.`,
              dzielnica: dz.nazwa,
              priority: 'low',
              priorityLabel: '🟢 Niski priorytet'
            });
          }
          

          if (dz.wydarzenia >= 3) {
            newProposals.push({
              type: 'success',
              typeLabel: 'Sukces',
              icon: '⭐',
              title: `Aktywna społeczność w ${dz.nazwa}`,
              description: `Dzielnica wyróżnia się ${dz.wydarzenia} wydarzeniami. Warto promować jako przykład dobrej praktyki.`,
              dzielnica: dz.nazwa,
              priority: 'low',
              priorityLabel: '🟢 Informacja'
            });
          }
        });
        
        const priorityOrder = { high: 0, medium: 1, low: 2 };
        newProposals.sort((a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]);
        
        this.proposals = newProposals;
        this.generatingProposals = false;
        this.proposalsGenerated = true;
      }, 1500);
    },

    analyzeInfrastructure() {
      this.analyzingInfrastructure = true;
      this.infrastructureAnalysis = [];
      
      setTimeout(() => {
        const analysis = [];
        
        if (!this.dzielnicaData) {
          this.analyzingInfrastructure = false;
          this.analysisCompleted = true;
          return;
        }
        

        this.dzielnicaData.features.forEach(f => {
          const nazwa = f.properties.nazwa;
          const mieszkancy = f.properties.liczba_mieszkancow || 0;
          
          const szkoly = this.szkolyData.filter(s => s.dzielnica === nazwa).length;
          const apteki = this.aptekiData.filter(a => a.dzielnica === nazwa).length;
          

          const normaSkoly = Math.ceil(mieszkancy / 3000);
          const normaApteki = Math.ceil(mieszkancy / 4000);
          

          if (szkoly < normaSkoly && mieszkancy > 200) {
            const niedobor = normaSkoly - szkoly;
            const ratio = mieszkancy > 0 && szkoly > 0 ? Math.round(mieszkancy / szkoly) : mieszkancy;
            

            let severity, severityLabel;
            if (szkoly === 0) {
              severity = 'extreme';
              severityLabel = '⚫ BRAK SZKÓŁ!';
            } else if (niedobor >= 2) {
              severity = 'critical';
              severityLabel = '🔴 Krytyczny';
            } else {
              severity = 'warning';
              severityLabel = '🟡 Średni';
            }
            
            analysis.push({
              type: 'szkola',
              icon: '🎓',
              dzielnica: nazwa,
              description: szkoly === 0 
                ? `⚠️ BRAK SZKÓŁ! ${mieszkancy.toLocaleString()} mieszkańców bez dostępu do szkoły. Zalecana liczba: ${normaSkoly}.`
                : `Brakuje ${niedobor} ${niedobor === 1 ? 'szkoły' : 'szkół'}. Aktualna liczba: ${szkoly}, zalecana: ${normaSkoly}.`,
              mieszkancy: mieszkancy,
              count: szkoly,
              ratio: szkoly === 0 ? 'BRAK' : `${ratio.toLocaleString()} mieszk./szkołę`,
              severity: severity,
              severityLabel: severityLabel,
              needed: niedobor
            });
          }
          

          if (apteki < normaApteki && mieszkancy > 200) {
            const niedobor = normaApteki - apteki;
            const ratio = mieszkancy > 0 && apteki > 0 ? Math.round(mieszkancy / apteki) : mieszkancy;
            

            let severity, severityLabel;
            if (apteki === 0) {
              severity = 'extreme';
              severityLabel = '⚫ BRAK APTEK!';
            } else if (niedobor >= 2) {
              severity = 'critical';
              severityLabel = '🔴 Krytyczny';
            } else {
              severity = 'warning';
              severityLabel = '🟡 Średni';
            }
            
            analysis.push({
              type: 'apteka',
              icon: '💊',
              dzielnica: nazwa,
              description: apteki === 0
                ? `⚠️ BRAK APTEK! ${mieszkancy.toLocaleString()} mieszkańców bez dostępu do apteki. Zalecana liczba: ${normaApteki}.`
                : `Brakuje ${niedobor} ${niedobor === 1 ? 'apteki' : 'aptek'}. Aktualna liczba: ${apteki}, zalecana: ${normaApteki}.`,
              mieszkancy: mieszkancy,
              count: apteki,
              ratio: apteki === 0 ? 'BRAK' : `${ratio.toLocaleString()} mieszk./aptekę`,
              severity: severity,
              severityLabel: severityLabel,
              needed: niedobor
            });
          }
        });
        

        analysis.sort((a, b) => {
          const order = { extreme: 0, critical: 1, warning: 2 };
          if (order[a.severity] !== order[b.severity]) {
            return order[a.severity] - order[b.severity];
          }

          return b.mieszkancy - a.mieszkancy;
        });
        
        this.infrastructureAnalysis = analysis;
        this.analyzingInfrastructure = false;
        this.analysisCompleted = true;
      }, 1200);
    },

    simulateNewPlace(item) {

      const dzielnicaFeature = this.dzielnicaData.features.find(
        f => f.properties.nazwa === item.dzielnica
      );
      
      if (!dzielnicaFeature) return;
      
      // Oblicz centroid dzielnicy (przybliżony)
      let lat = 0, lng = 0, count = 0;
      const coords = dzielnicaFeature.geometry.type === 'Polygon' 
        ? dzielnicaFeature.geometry.coordinates[0]
        : dzielnicaFeature.geometry.coordinates[0][0];
      
      coords.forEach(coord => {
        lng += coord[0];
        lat += coord[1];
        count++;
      });
      
      lat = lat / count + (Math.random() - 0.5) * 0.01;
      lng = lng / count + (Math.random() - 0.5) * 0.01;
      
      // Dodaj symulowaną lokalizację
      const newPlace = {
        type: item.type,
        nazwa: item.type === 'szkola' 
          ? `Nowa Szkoła w ${item.dzielnica}` 
          : `Nowa Apteka w ${item.dzielnica}`,
        dzielnica: item.dzielnica,
        lat: lat,
        lng: lng
      };
      
      this.simulatedPlaces.push(newPlace);
      this.displaySimulatedMarkers();
      
      // Zoom do dzielnicy
      this.zoomToDzielnica(item.dzielnica);
    },

    displaySimulatedMarkers() {
      // Usuń poprzednie markery symulacji
      if (this.simulatedMarkersLayer) {
        this.map.removeLayer(this.simulatedMarkersLayer);
      }
      
      const markers = [];
      
      this.simulatedPlaces.forEach(place => {
        // Stwórz pulsującą ikonę dla symulacji
        const iconHtml = `
          <div class="simulated-marker ${place.type}">
            <span class="marker-icon">${place.type === 'szkola' ? '🎓' : '💊'}</span>
            <span class="marker-pulse"></span>
          </div>
        `;
        
        const customIcon = L.divIcon({
          html: iconHtml,
          className: 'simulated-marker-container',
          iconSize: [40, 40],
          iconAnchor: [20, 20],
        });
        
        const marker = L.marker([place.lat, place.lng], { icon: customIcon });
        
        marker.bindPopup(`
          <div style="text-align: center;">
            <strong style="color: #e67e22;">📍 SYMULACJA</strong><br>
            <span style="font-size: 24px;">${place.type === 'szkola' ? '🎓' : '💊'}</span><br>
            <strong>${place.nazwa}</strong><br>
            <small style="color: #7f8c8d;">${place.dzielnica}</small><br>
            <em style="font-size: 11px; color: #95a5a6;">Proponowana lokalizacja</em>
          </div>
        `);
        
        markers.push(marker);
      });
      
      this.simulatedMarkersLayer = L.layerGroup(markers).addTo(toRaw(this.map));
      
      // Odśwież heat mapę jeśli jest włączona
      if (this.wazneMiejscaHeatmap) {
        this.showWazneMiejscaHeatmap();
      }
    },

    removeSimulatedPlace(index) {
      this.simulatedPlaces.splice(index, 1);
      this.displaySimulatedMarkers();
    },

    clearAllSimulations() {
      this.simulatedPlaces = [];
      if (this.simulatedMarkersLayer) {
        this.map.removeLayer(this.simulatedMarkersLayer);
        this.simulatedMarkersLayer = null;
      }
      // Odśwież heat mapę jeśli jest włączona
      if (this.wazneMiejscaHeatmap) {
        this.showWazneMiejscaHeatmap();
      }
    },

    async loadDzielnice() {
      try {
        const response = await axios.get(API_URL);
        this.dzielnicaData = response.data;
        this.addGeoJSONLayer(response.data);
      } catch (err) {
        console.error("Błąd ładowania danych dzielnic:", err);
      }
    },

    get_last_upadate_time() {
      if (this.transportData) {
        return this.transportData.lastUpdate;
      } else {
        return "";
      }
    },

    getPopulationByDemography(props) {
      const gender = this.selectedDemography;
      const age = this.selectedAge;

      if (age !== "all") {
        if (gender === "kobiety") {
          return props[`kobiety_${age}`] || 0;
        } else if (gender === "mezczyzni") {
          return props[`mezczyzni_${age}`] || 0;
        } else {
          return (
            (props[`kobiety_${age}`] || 0) + (props[`mezczyzni_${age}`] || 0)
          );
        }
      }

      if (gender === "kobiety") {
        return props.liczba_kobiet || 0;
      } else if (gender === "mezczyzni") {
        return props.liczba_mezczyzn || 0;
      }
      return props.liczba_mieszkancow || 0;
    },

    getColorForPopulation(population) {
      return population > 30000
        ? "#08306b"
        : population > 20000
        ? "#2171b5"
        : population > 15000
        ? "#4292c6"
        : population > 10000
        ? "#6baed6"
        : population > 5000
        ? "#9ecae1"
        : population > 1000
        ? "#c6dbef"
        : "#deebf7";
    },

    getColorForGender(population) {
      return population > 15000
        ? "#08306b"
        : population > 10000
        ? "#2171b5"
        : population > 7500
        ? "#4292c6"
        : population > 5000
        ? "#6baed6"
        : population > 2500
        ? "#9ecae1"
        : population > 500
        ? "#c6dbef"
        : "#deebf7";
    },

    getColorForAgeGroup(population) {
      return population > 4000
        ? "#08306b"
        : population > 3000
        ? "#2171b5"
        : population > 2000
        ? "#4292c6"
        : population > 1000
        ? "#6baed6"
        : population > 500
        ? "#9ecae1"
        : population > 100
        ? "#c6dbef"
        : "#deebf7";
    },

    getColor(population) {
      if (this.selectedAge !== "all") {
        return this.getColorForAgeGroup(population);
      }
      if (this.selectedDemography === "all") {
        return this.getColorForPopulation(population);
      }
      return this.getColorForGender(population);
    },

    style(feature) {
      const pop = this.getPopulationByDemography(feature.properties);
      return {
        fillColor: this.getColor(pop),
        weight: 2,
        opacity: 1,
        color: "#fff",
        dashArray: "3",
        fillOpacity: 0.7,
      };
    },

    highlightFeature(e) {
      const layer = e.target;

      layer.setStyle({
        weight: 4,
        color: "#2c3e50",
        dashArray: "",
        fillOpacity: 0.9,
      });

      layer.bringToFront();

      this.hoveredDzielnica = layer.feature.properties;
    },

    resetHighlight(e) {
      this.geojsonLayer.resetStyle(e.target);
      this.hoveredDzielnica = null;
    },

    zoomToFeature(e) {
      this.map.fitBounds(e.target.getBounds());
    },

    onEachFeature(feature, layer) {
      layer.on({
        mouseover: this.highlightFeature,
        mouseout: this.resetHighlight,
        click: this.zoomToFeature,
      });
    },

    addGeoJSONLayer(data) {
      if (this.geojsonLayer) {
        this.map.removeLayer(this.geojsonLayer);
      }

      this.geojsonLayer = L.geoJSON(data, {
        style: this.style.bind(this),
        onEachFeature: this.onEachFeature.bind(this),
      }).addTo(toRaw(this.map));

      if (this.geojsonLayer.getBounds().isValid()) {
        this.map.fitBounds(this.geojsonLayer.getBounds());
      }
    },

    refreshMap() {
      if (!this.dzielnicaData) return;

      if (this.geojsonLayer) {
        this.map.removeLayer(this.geojsonLayer);
        this.geojsonLayer = null;
      }

      const self = this;
      const category = this.activeCategory;

      this.geojsonLayer = L.geoJSON(this.dzielnicaData, {
        style: (feature) => {
          let value;
          if (category === 2) {
            value = self.calculateDensityByDemography(feature.properties);
          } else if (category === 3) {
            value = feature.properties.powierzchnia;
          } else {
            value = self.getPopulationByDemography(feature.properties);
          }
          return {
            fillColor: self.currentColorFunction(value),
            weight: 2,
            opacity: 1,
            color: "#fff",
            dashArray: "3",
            fillOpacity: 0.7,
          };
        },
        onEachFeature: this.onEachFeature.bind(this),
      }).addTo(toRaw(this.map));
    },

    clearAllLayers() {
      if (this.geojsonLayer) {
        this.map.removeLayer(this.geojsonLayer);
        this.geojsonLayer = null;
      }
      if (this.zdarzeniaLayer) {
        this.map.removeLayer(this.zdarzeniaLayer);
        this.zdarzeniaLayer = null;
      }
      if (this.transportLayer) {
        this.map.removeLayer(this.transportLayer);
        this.transportLayer = null;
      }
      if (this.routeLayer) {
        this.map.removeLayer(this.routeLayer);
        this.routeLayer = null;
      }
      if (this.locationMarker) {
        this.map.removeLayer(this.locationMarker);
        this.locationMarker = null;
      }
      if (this.dzielnicaBackgroundLayer) {
        this.map.removeLayer(this.dzielnicaBackgroundLayer);
        this.dzielnicaBackgroundLayer = null;
      }
      if (this.highlightedDzielnicaLayer) {
        this.map.removeLayer(this.highlightedDzielnicaLayer);
        this.highlightedDzielnicaLayer = null;
      }
      if (this.heatmapLayer) {
        this.map.removeLayer(this.heatmapLayer);
        this.heatmapLayer = null;
      }
      if (this.wazneMiejscaLayer) {
        this.map.removeLayer(this.wazneMiejscaLayer);
        this.wazneMiejscaLayer = null;
      }
      if (this.wazneMiejscaBackgroundLayer) {
        this.map.removeLayer(this.wazneMiejscaBackgroundLayer);
        this.wazneMiejscaBackgroundLayer = null;
      }
      if (this.wazneMiejscaHeatmapLayer) {
        this.map.removeLayer(this.wazneMiejscaHeatmapLayer);
        this.wazneMiejscaHeatmapLayer = null;
      }
      if (this.simulatedMarkersLayer) {
        this.map.removeLayer(this.simulatedMarkersLayer);
        this.simulatedMarkersLayer = null;
      }
      this.simulatedPlaces = [];
      this.hoveredDzielnicaSpolecznosc = null;
      this.hoveredDzielnicaWazneMiejsca = null;
      this.heatmapEnabled = false;
      this.wazneMiejscaHeatmap = false;
    },

    pointInPolygon(point, polygon) {
      const x = point[0];
      const y = point[1];
      let inside = false;

      for (let i = 0, j = polygon.length - 1; i < polygon.length; j = i++) {
        const xi = polygon[i][0],
          yi = polygon[i][1];
        const xj = polygon[j][0],
          yj = polygon[j][1];

        if (yi > y !== yj > y && x < ((xj - xi) * (y - yi)) / (yj - yi) + xi) {
          inside = !inside;
        }
      }

      return inside;
    },

    findDzielnicaForPoint(lat, lng) {
      if (!this.dzielnicaData || !this.dzielnicaData.features) return null;

      for (const feature of this.dzielnicaData.features) {
        const geometry = feature.geometry;
        const nazwa = feature.properties.nazwa;

        if (geometry.type === "Polygon") {
          if (this.pointInPolygon([lng, lat], geometry.coordinates[0])) {
            return nazwa;
          }
        } else if (geometry.type === "MultiPolygon") {
          for (const poly of geometry.coordinates) {
            if (this.pointInPolygon([lng, lat], poly[0])) {
              return nazwa;
            }
          }
        }
      }

      return null;
    },

    zoomToDzielnica(nazwa) {
      if (!this.dzielnicaData) return;

      const feature = this.dzielnicaData.features.find(
        (f) => f.properties.nazwa === nazwa
      );

      if (feature) {
        const layer = L.geoJSON(feature);
        this.map.fitBounds(layer.getBounds(), { padding: [50, 50] });
      }
    },

    highlightDzielnicaOnMap(nazwa) {
      this.unhighlightDzielnicaOnMap();

      if (!this.dzielnicaData) return;

      const feature = this.dzielnicaData.features.find(
        (f) => f.properties.nazwa === nazwa
      );

      if (feature) {
        this.highlightedDzielnicaLayer = L.geoJSON(feature, {
          style: {
            fillColor: "#f39c12",
            weight: 3,
            opacity: 1,
            color: "#e67e22",
            fillOpacity: 0.3,
          },
        }).addTo(toRaw(this.map));

        this.hoveredDzielnicaSpolecznosc = nazwa;
      }
    },

    unhighlightDzielnicaOnMap() {
      if (this.highlightedDzielnicaLayer) {
        this.map.removeLayer(this.highlightedDzielnicaLayer);
        this.highlightedDzielnicaLayer = null;
      }
      this.hoveredDzielnicaSpolecznosc = null;
    },

    toggleHeatmap() {
      this.heatmapEnabled = !this.heatmapEnabled;
      if (this.heatmapEnabled) {
        this.showHeatmap();

      } else {
        this.hideHeatmap();
      }
    },

    showHeatmap() {
      this.hideHeatmap();

      if (!this.zdarzeniaData || !this.zdarzeniaData.features) return;

      const filteredFeatures = this.zdarzeniaData.features.filter((f) => {
        if (
          this.spolecznoscFilter !== "all" &&
          f.properties.kategoria2 !== this.spolecznoscFilter
        ) {
          return false;
        }
        if (this.userAge !== null) {
          const minWiek = f.properties.min_wiek || 0;
          if (this.userAge < minWiek) {
            return false;
          }
        }
        return true;
      });

      const heatData = filteredFeatures.map((f) => {
        const coords = f.geometry.coordinates;

        const intensity = Math.max(
          1,
          (f.properties.like || 0) - (f.properties.dislike || 0) + 1
        );
        return [coords[1], coords[0], intensity];
      });

      if (heatData.length > 0) {
        this.heatmapLayer = L.heatLayer(heatData, {
          minOpacity: 1,
          radius: 20,
          blur: 30,
          maxZoom: 17,
          max: 1,
          gradient: {
            0.0: "#3498db",
            0.3: "#2ecc71",
            0.5: "#f1c40f",
            0.7: "#e67e22",
            1.0: "#e74c3c",
          },
        }).addTo(toRaw(this.map));
      }
    },

    hideHeatmap() {
      if (this.heatmapLayer) {
        this.map.removeLayer(this.heatmapLayer);
        this.heatmapLayer = null;
      }
    },


    resetDzielnicaBackgroundColor() {
      // Przywróć oryginalny styl
      if (this.dzielnicaBackgroundLayer) {
        this.dzielnicaBackgroundLayer.eachLayer((layer) => {
          layer.setStyle({
            fillColor: "#3498db",
            weight: 1,
            opacity: 0.3,
            color: "#2c3e50",
            fillOpacity: 0.05,
          });
        });
      }
    },





    parseKoordynaty(str) {
      if (!str) return null;
      const parts = str.replace(/[NE]/g, "").split(",");
      if (parts.length !== 2) return null;
      const lat = parseFloat(parts[0].trim());
      const lng = parseFloat(parts[1].trim());
      if (isNaN(lat) || isNaN(lng)) return null;
      return { lat, lng };
    },

    async loadWazneMiejsca() {
      try {
        const [szkolyRes, aptekiRes] = await Promise.all([
          axios.get("/data/szkoly.json"),
          axios.get("/data/apteki.json"),
        ]);

        this.szkolyData = szkolyRes.data
          .map((item, idx) => {
            const coords = this.parseKoordynaty(item.koordynaty);
            const dzielnica = coords
              ? this.findDzielnicaForPoint(coords.lat, coords.lng)
              : null;
            return {
              id: "szkola_" + idx,
              typ: "szkola",
              podtyp: item.typ,
              nazwa: item.Nazwa,
              opis: item.Opis,
              lat: coords?.lat,
              lng: coords?.lng,
              dzielnica,
            };
          })
          .filter((item) => item.lat && item.lng);

        this.aptekiData = aptekiRes.data
          .map((item, idx) => {
            const coords = this.parseKoordynaty(item.koordynaty);
            const dzielnica = coords
              ? this.findDzielnicaForPoint(coords.lat, coords.lng)
              : null;
            return {
              id: "apteka_" + idx,
              typ: "apteka",
              nazwa: item.tytul,
              opis: item.opis,
              lat: coords?.lat,
              lng: coords?.lng,
              dzielnica,
            };
          })
          .filter((item) => item.lat && item.lng);

        this.displayWazneMiejsca();
      } catch (err) {
        console.error("Błąd ładowania ważnych miejsc:", err);
      }
    },

    displayWazneMiejsca() {
      if (this.wazneMiejscaLayer) {
        this.map.removeLayer(this.wazneMiejscaLayer);
      }

      let data = [];
      if (
        this.wazneMiejscaFilter === "all" ||
        this.wazneMiejscaFilter === "szkoly"
      ) {
        data = data.concat(this.szkolyData);
      }
      if (
        this.wazneMiejscaFilter === "all" ||
        this.wazneMiejscaFilter === "apteki"
      ) {
        data = data.concat(this.aptekiData);
      }

      const markers = [];

      data.forEach((item) => {
        const iconUrl =
          item.typ === "szkola"
            ? "/images/education.png"
            : "/images/healthcare.png";

        const customIcon = L.icon({
          iconUrl: iconUrl,
          iconSize: [28, 28],
          iconAnchor: [14, 28],
          popupAnchor: [0, -28],
        });

        const marker = L.marker([item.lat, item.lng], { icon: customIcon });

        const popupContent = `
          <div style="min-width: 200px;">
            <strong>${item.nazwa}</strong><br>
            <em style="color: ${item.typ === "szkola" ? "#3498db" : "#27ae60"}">
              ${item.typ === "szkola" ? "🎓 Szkoła" : "💊 Apteka"}
              ${item.podtyp ? ` - ${item.podtyp}` : ""}
            </em><br>
            ${
              item.dzielnica
                ? `<small style="color: #7f8c8d;">📍 ${item.dzielnica}</small><br>`
                : ""
            }
            <p style="margin: 5px 0; font-size: 12px;">${item.opis}</p>
          </div>
        `;

        marker.bindPopup(popupContent);
        markers.push(marker);
      });

      this.wazneMiejscaLayer = L.layerGroup(markers).addTo(toRaw(this.map));
    },

    addWazneMiejscaBackgroundLayer() {
      if (!this.dzielnicaData) return;

      if (this.wazneMiejscaBackgroundLayer) {
        this.map.removeLayer(this.wazneMiejscaBackgroundLayer);
      }

      const self = this;
      this.wazneMiejscaBackgroundLayer = L.geoJSON(this.dzielnicaData, {
        style: () => ({
          fillColor: "#9b59b6",
          weight: 1,
          opacity: 0.3,
          color: "#8e44ad",
          fillOpacity: 0.05,
        }),
        onEachFeature: (feature, layer) => {
          layer.on({
            mouseover: (e) => {
              const l = e.target;
              l.setStyle({
                fillOpacity: 0.2,
                weight: 2,
              });
              self.hoveredDzielnicaWazneMiejsca = feature.properties.nazwa;
            },
            mouseout: (e) => {
              self.wazneMiejscaBackgroundLayer.resetStyle(e.target);
              self.hoveredDzielnicaWazneMiejsca = null;
            },
          });
        },
      }).addTo(toRaw(this.map));
    },

    toggleWazneMiejscaHeatmap() {
      this.wazneMiejscaHeatmap = !this.wazneMiejscaHeatmap;
      if (this.wazneMiejscaHeatmap) {
        this.showWazneMiejscaHeatmap();

      } else {
        this.hideWazneMiejscaHeatmap();

      }
    },

    showWazneMiejscaHeatmap() {
      this.hideWazneMiejscaHeatmap();

      let data = [];
      if (
        this.wazneMiejscaFilter === "all" ||
        this.wazneMiejscaFilter === "szkoly"
      ) {
        data = data.concat(this.szkolyData);
        // Dodaj symulowane szkoły
        const symulowaneSzkoly = this.simulatedPlaces
          .filter(p => p.type === 'szkola')
          .map(p => ({ lat: p.lat, lng: p.lng, simulated: true }));
        data = data.concat(symulowaneSzkoly);
      }
      if (
        this.wazneMiejscaFilter === "all" ||
        this.wazneMiejscaFilter === "apteki"
      ) {
        data = data.concat(this.aptekiData);
        // Dodaj symulowane apteki
        const symulowaneApteki = this.simulatedPlaces
          .filter(p => p.type === 'apteka')
          .map(p => ({ lat: p.lat, lng: p.lng, simulated: true }));
        data = data.concat(symulowaneApteki);
      }

      // Symulowane miejsca mają większą intensywność (wyróżnienie)
      const heatData = data.map((item) => [item.lat, item.lng, item.simulated ? 1.5 : 1]);

      if (heatData.length > 0) {
        this.wazneMiejscaHeatmapLayer = L.heatLayer(heatData, {
          minOpacity: 0.5,
          radius: 40,
          blur: 25,
          maxZoom: 17,
          max: 1.5,
          gradient: {
            0.0: "#9b59b6",
            0.3: "#3498db",
            0.5: "#2ecc71",
            0.7: "#f1c40f",
            1.0: "#e74c3c",
          },
        }).addTo(toRaw(this.map));
      }
    },

    hideWazneMiejscaHeatmap() {
      if (this.wazneMiejscaHeatmapLayer) {
        this.map.removeLayer(this.wazneMiejscaHeatmapLayer);
        this.wazneMiejscaHeatmapLayer = null;
      }
    },

    addDzielnicaBackgroundLayer() {
      if (!this.dzielnicaData) return;

      if (this.dzielnicaBackgroundLayer) {
        this.map.removeLayer(this.dzielnicaBackgroundLayer);
      }

      const self = this;
      this.dzielnicaBackgroundLayer = L.geoJSON(this.dzielnicaData, {
        style: () => ({
          fillColor: "#3498db",
          weight: 1,
          opacity: 0.3,
          color: "#2c3e50",
          fillOpacity: 0.05,
        }),
        onEachFeature: (feature, layer) => {
          layer.on({
            mouseover: (e) => {
              const l = e.target;
              l.setStyle({
                fillOpacity: 0.2,
                weight: 2,
              });
              self.hoveredDzielnicaSpolecznosc = feature.properties.nazwa;
            },
            mouseout: (e) => {
              self.dzielnicaBackgroundLayer.resetStyle(e.target);
              self.hoveredDzielnicaSpolecznosc = null;
            },
          });
        },
      }).addTo(toRaw(this.map));
    },

    toggleSection(section) {
      if (this.activeSection === section) {
        this.clearAllLayers();
        this.map.off("click", this.onMapClick);
        this.activeSection = null;
        return;
      }
      let interval_transport;

      this.clearAllLayers();
      this.map.off("click", this.onMapClick);

      this.activeSection = section;

      clearInterval(interval_transport);

      if (section === "demografia") {
        this.refreshMap();
      } else if (section === "spolecznosc") {
        this.addDzielnicaBackgroundLayer();
        this.loadZdarzenia();
        this.map.on("click", this.onMapClick);
      } else if (section === "transport") {
        this.loadTransport();
        interval_transport = setInterval(this.loadTransport, 15000);
      } else if (section === "zdrowie") {
        this.loadWazneMiejsca();
        this.addWazneMiejscaBackgroundLayer();
      }
    },

    onMapClick(e) {
      if (this.activeSection !== "spolecznosc") return;

      const { lat, lng } = e.latlng;

      const dzielnica = this.findDzielnicaForPoint(lat, lng);

      this.noweZdarzenie.lokalizacja_lat = lat;
      this.noweZdarzenie.lokalizacja_lng = lng;
      this.noweZdarzenie.dzielnica = dzielnica;

      if (this.locationMarker) {
        this.map.removeLayer(this.locationMarker);
      }

      var markerIcon = L.icon({
        iconUrl: dzielnica ? "/images/pin.png" : "/images/pin.png",
        shadowUrl: "",
        iconSize: [40, 40],
        shadowSize: [50, 64],
        iconAnchor: [20, 20],
        shadowAnchor: [4, 62],
        popupAnchor: [-3, -76],
      });

      this.locationMarker = L.marker([lat, lng], { icon: markerIcon }).addTo(
        toRaw(this.map)
      );

      if (dzielnica) {
        this.locationMarker
          .bindPopup(`<strong>Dzielnica:</strong> ${dzielnica}`)
          .openPopup();
      } else {
        this.locationMarker
          .bindPopup(
            `<strong style="color: #e74c3c;">⚠️ Poza obszarem Gdańska</strong>`
          )
          .openPopup();
      }
    },

    async loadZdarzenia() {
      try {
        const response = await axios.get(
          "http://localhost:8000/api/zdarzenia-geojson/"
        );
        this.zdarzeniaData = response.data;
        this.displayZdarzenia();
      } catch (err) {
        console.error("Błąd ładowania zdarzeń:", err);
      }
    },

    async loadTransport() {
      if (!(this.activeSection === "transport")) {
        return;
      }
      fetch("https://ckan2.multimediagdansk.pl/gpsPositions?v=2")
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          return response.json();
        })
        .then((data) => {
          this.transportData = data;
          console.log("data:", data);
          this.displayTransport();
        })
        .catch((error) => {
          console.error("error transport:", error);
        });
    },

    displayTransport() {
      if (this.transportLayer) {
        this.map.removeLayer(this.transportLayer);
      }

      if (!this.transportData || !this.transportData.vehicles) return;

      const vehicles = this.transportData.vehicles;
      const markers = [];

      vehicles.forEach((vehicle) => {
        let color = "#3498db";
        if (vehicle.delay > 2) {
          color = "#e74c3c";
        } else if (vehicle.delay < -1) {
          color = "#2ecc71";
        }

        const marker = L.circleMarker([vehicle.lat, vehicle.lon], {
          radius: 8,
          fillColor: color,
          color: "#fff",
          weight: 2,
          opacity: 1,
          fillOpacity: 0.8,
        });

        let delayText = "Punktualnie";
        if (vehicle.delay > 0) {
          delayText = `Opóźnienie: +${Math.round(vehicle.delay / 60)} min`;
        } else if (vehicle.delay < 0) {
          delayText = `Przed czasem: ${Math.round(vehicle.delay / 60)} min`;
        }

        const popupContent = `
          <div class="transport-popup">
            <h4 style="margin: 0 0 5px 0; color: #2c3e50;">
              🚌 Linia ${vehicle.routeShortName}
            </h4>
            <p style="margin: 3px 0; font-weight: bold;">${
              vehicle.headsign || "Brak kierunku"
            }</p>
            <hr style="margin: 8px 0; border: none; border-top: 1px solid #eee;">
            <p style="margin: 3px 0;"><strong>Pojazd:</strong> ${
              vehicle.vehicleCode
            }</p>
            <p style="margin: 3px 0;"><strong>Prędkość:</strong> ${
              vehicle.speed
            } km/h</p>
            <p style="margin: 3px 0; color: ${color};"><strong>${delayText}</strong></p>
            <p style="margin: 3px 0; font-size: 11px; color: #888;">
              ID: ${vehicle.vehicleId} | Kurs: ${vehicle.vehicleService}
            </p>
            
          </div>
        `;

        const self = this;
        marker.bindPopup(popupContent);
        marker.on("popupopen", function () {
          self.showTransportRoute(vehicle.routeId, vehicle.tripId);
        });
        marker.on("popupclose", function () {
          self.hideTransportRoute();
        });
        markers.push(marker);
      });

      this.transportLayer = L.layerGroup(markers).addTo(toRaw(this.map));
    },

    showTransportRoute(routeId, tripId) {
      this.hideTransportRoute();

      const date = new Date();
      const formattedDate = date.toISOString().split("T")[0];

      fetch(
        `https://ckan2.multimediagdansk.pl/shapes?date=${formattedDate}&routeId=${routeId}&tripId=${tripId}`
      )
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          if (data && data.coordinates) {
            const latLngs = data.coordinates.map((coord) => [
              coord[1],
              coord[0],
            ]);

            this.routeLayer = L.polyline(latLngs, {
              color: "#3498db",
              weight: 4,
              opacity: 0.8,
              dashArray: "10, 10",
            }).addTo(toRaw(this.map));
          }
        })
        .catch((error) => {
          console.error("Błąd pobierania trasy:", error);
        });
    },

    hideTransportRoute() {
      if (this.routeLayer) {
        toRaw(this.map).removeLayer(toRaw(this.routeLayer));
        this.routeLayer = null;
      }
    },

    getIconForKategoria(kategoria3) {
      const kat = this.wszystkieKategorie.find((k) => k.id === kategoria3);
      if (kat) {
        return `/images/${kat.icon}`;
      }
      return "/images/pin.png";
    },

    getKategoriaName(kategoria3) {
      const kat = this.wszystkieKategorie.find((k) => k.id === kategoria3);
      return kat ? kat.name : kategoria3;
    },

    displayZdarzenia() {
      if (this.zdarzeniaLayer) {
        toRaw(this.map).removeLayer(this.zdarzeniaLayer);
      }

      if (!this.zdarzeniaData) return;

      const filteredFeatures = this.zdarzeniaData.features.filter((f) => {

        if (
          this.spolecznoscFilter !== "all" &&
          f.properties.kategoria2 !== this.spolecznoscFilter
        ) {
          return false;
        }

        if (this.userAge !== null) {
          const minWiek = f.properties.min_wiek || 0;
          if (this.userAge < minWiek) {
            return false;
          }
        }
        return true;
      });

      const filteredData = {
        type: "FeatureCollection",
        features: filteredFeatures,
      };

      const self = this;

      this.zdarzeniaLayer = L.geoJSON(filteredData, {
        pointToLayer: (feature, latlng) => {
          const kategoria3 = feature.properties.kategoria3;
          const iconUrl = self.getIconForKategoria(kategoria3);

          const likes = feature.properties.like || 0;
          const dislikes = feature.properties.dislike || 0;
          const popularity = likes - dislikes;

          const baseSize = 24;
          const sizePerPoint = 2;
          const maxSize = 48;
          const minSize = 20;

          let iconSize = baseSize + popularity * sizePerPoint;
          iconSize = Math.max(minSize, Math.min(maxSize, iconSize));

          const customIcon = L.icon({
            iconUrl: iconUrl,
            iconSize: [iconSize, iconSize],
            iconAnchor: [iconSize / 2, iconSize],
            popupAnchor: [0, -iconSize],
          });

          return L.marker(latlng, { icon: customIcon });
        },
        onEachFeature: (feature, layer) => {
          const p = feature.properties;
          const hasVoted = self.hasVotedOn(p.id);
          const kategoriaName = self.getKategoriaName(p.kategoria3);

          const minWiekInfo =
            p.min_wiek > 0
              ? `<small style="color: #e67e22; display: block; margin-top: 4px;">🔞 Min. wiek: ${p.min_wiek} lat</small>`
              : "";
          const niepelnosprawniInfo = p.dla_niepelnosprawnych
            ? `<small style="color: #27ae60; display: block; margin-top: 2px;">♿ Dostosowane dla niepełnosprawnych</small>`
            : "";

          const popupContent = document.createElement("div");
          popupContent.innerHTML = `
            <strong>${p.tytul}</strong><br>
            <em>${
              p.kategoria2 === "zgloszenie" ? "🔴 Zgłoszenie" : "🟢 Wydarzenie"
            }</em>
            <span style="margin-left: 8px; background: #ecf0f1; padding: 2px 6px; border-radius: 3px; font-size: 11px;">${kategoriaName}</span><br>
            ${
              p.dzielnica
                ? `<small style="color: #7f8c8d;">📍 ${p.dzielnica}</small><br>`
                : ""
            }
            ${minWiekInfo}
            ${niepelnosprawniInfo}
            <p style="margin: 5px 0;">${p.opis}</p>
            <div style="margin-top: 10px; display: flex; gap: 10px; align-items: center;">
              <button class="vote-btn like-btn" data-id="${p.id}" ${
            hasVoted ? "disabled" : ""
          }>
                👍 <span class="like-count">${p.like}</span>
              </button>
              <button class="vote-btn dislike-btn" data-id="${p.id}" ${
            hasVoted ? "disabled" : ""
          }>
                👎 <span class="dislike-count">${p.dislike}</span>
              </button>
              ${
                hasVoted
                  ? '<small style="color: #888;">Już głosowałeś</small>'
                  : ""
              }
            </div>
          `;

          const likeBtn = popupContent.querySelector(".like-btn");
          const dislikeBtn = popupContent.querySelector(".dislike-btn");

          likeBtn.addEventListener("click", () =>
            self.voteOnZdarzenie(p.id, "like", popupContent)
          );
          dislikeBtn.addEventListener("click", () =>
            self.voteOnZdarzenie(p.id, "dislike", popupContent)
          );

          layer.bindPopup(popupContent);

          layer.on("click", () => {
            self.openKomentarzePanel(p);
          });
        },
      }).addTo(toRaw(this.map));
    },

    async openKomentarzePanel(zdarzenie) {
      this.selectedZdarzenie = zdarzenie;
      this.komentarze = [];
      this.nowyKomentarz = { autor: "", tresc: "" };

      try {
        const response = await axios.get(
          `http://localhost:8000/api/zdarzenia/${zdarzenie.id}/komentarze/`
        );
        this.komentarze = response.data;
      } catch (err) {
        console.error("Błąd ładowania komentarzy:", err);
      }
    },

    closeKomentarzePanel() {
      this.selectedZdarzenie = null;
      this.komentarze = [];
    },

    async submitKomentarz() {
      if (!this.nowyKomentarz.tresc.trim() || !this.selectedZdarzenie) return;

      try {
        const data = {
          zdarzenie: this.selectedZdarzenie.id,
          autor: this.nowyKomentarz.autor.trim() || "Anonim",
          tresc: this.nowyKomentarz.tresc.trim(),
        };

        await axios.post("http://localhost:8000/api/komentarze/", data);

        const response = await axios.get(
          `http://localhost:8000/api/zdarzenia/${this.selectedZdarzenie.id}/komentarze/`
        );
        this.komentarze = response.data;

        this.nowyKomentarz = { autor: "", tresc: "" };
      } catch (err) {
        console.error("Błąd dodawania komentarza:", err);
      }
    },

    formatKomentarzDate(dateStr) {
      if (!dateStr) return "";
      const date = new Date(dateStr);
      return date.toLocaleDateString("pl-PL", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    },

    setCookie(name, value, days) {
      const expires = new Date();
      expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
      document.cookie = `${name}=${value};expires=${expires.toUTCString()};path=/`;
    },

    getCookie(name) {
      const nameEQ = name + "=";
      const ca = document.cookie.split(";");
      for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === " ") c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0)
          return c.substring(nameEQ.length, c.length);
      }
      return null;
    },

    hasVotedOn(zdarzenieId) {
      const voted = this.getCookie("voted_zdarzenia") || "";
      return voted.split(",").includes(String(zdarzenieId));
    },

    markAsVoted(zdarzenieId) {
      let voted = this.getCookie("voted_zdarzenia") || "";
      const votedArray = voted ? voted.split(",") : [];
      if (!votedArray.includes(String(zdarzenieId))) {
        votedArray.push(String(zdarzenieId));
        this.setCookie("voted_zdarzenia", votedArray.join(","), 365);
      }
    },

    async voteOnZdarzenie(zdarzenieId, voteType, popupContent) {
      if (this.hasVotedOn(zdarzenieId)) {
        return;
      }

      try {
        const response = await axios.post(
          `${ZDARZENIA_API_URL}${zdarzenieId}/${voteType}/`
        );

        this.markAsVoted(zdarzenieId);

        const countSpan = popupContent.querySelector(`.${voteType}-count`);
        if (countSpan) {
          countSpan.textContent = response.data[voteType];
        }

        const buttons = popupContent.querySelectorAll(".vote-btn");
        buttons.forEach((btn) => (btn.disabled = true));

        const voteDiv = popupContent.querySelector(
          'div[style*="display: flex"]'
        );
        if (voteDiv && !voteDiv.querySelector("small")) {
          const small = document.createElement("small");
          small.style.color = "#888";
          small.textContent = "Już głosowałeś";
          voteDiv.appendChild(small);
        }
      } catch (err) {
        console.error("Błąd głosowania:", err);
      }
    },

    async submitZdarzenie() {
      if (!this.noweZdarzenie.lokalizacja_lat) {
        this.formMessage = "Wybierz lokalizację na mapie!";
        return;
      }

      if (!this.noweZdarzenie.dzielnica) {
        this.formMessage = "Lokalizacja musi być w obrębie dzielnicy Gdańska!";
        return;
      }

      try {
        const data = {
          lokalizacja_lat: this.noweZdarzenie.lokalizacja_lat,
          lokalizacja_lng: this.noweZdarzenie.lokalizacja_lng,
          dzielnica_nazwa: this.noweZdarzenie.dzielnica,
          kategoria2: this.noweZdarzenie.kategoria2,
          kategoria3: this.noweZdarzenie.kategoria3,
          tytul: this.noweZdarzenie.tytul,
          opis: this.noweZdarzenie.opis,
          termin_od: this.noweZdarzenie.termin_od || null,
          termin_do: this.noweZdarzenie.termin_do || null,
          min_wiek: this.noweZdarzenie.min_wiek || 0,
          dla_niepelnosprawnych:
            this.noweZdarzenie.kategoria2 === "wydarzenie"
              ? this.noweZdarzenie.dla_niepelnosprawnych
              : false,
        };

        await axios.post(ZDARZENIA_API_URL, data);

        this.formMessage = "Zdarzenie dodane pomyślnie!";

        this.noweZdarzenie = {
          lokalizacja_lat: null,
          lokalizacja_lng: null,
          dzielnica: null,
          kategoria2: "",
          kategoria3: "",
          tytul: "",
          opis: "",
          termin_od: "",
          termin_do: "",
          min_wiek: 0,
          dla_niepelnosprawnych: false,
        };

        if (this.locationMarker) {
          this.map.removeLayer(this.locationMarker);
          this.locationMarker = null;
        }

        this.loadZdarzenia();

        setTimeout(() => {
          this.formMessage = "";
        }, 3000);
      } catch (err) {
        console.error("Błąd dodawania zdarzenia:", err);
        this.formMessage = "Błąd podczas dodawania zdarzenia!";
      }
    },

    selectCategory(id) {
      this.activeCategory = this.activeCategory === id ? null : id;
      this.updateLegend();
      this.refreshMap();
    },

    selectDemography(id) {
      this.selectedDemography = id;
      this.updateLegend();
      this.refreshMap();
    },

    selectAge(id) {
      this.selectedAge = id;
      this.updateLegend();
      this.refreshMap();
    },

    updateLegend() {
      const isGender = this.selectedDemography !== "all";
      const isAge = this.selectedAge !== "all";

      if (this.activeCategory === 2) {
        this.legendItems = [
          { color: "#08306b", label: "> 10 000" },
          { color: "#2171b5", label: "5 000 – 10 000" },
          { color: "#4292c6", label: "3 000 – 5 000" },
          { color: "#6baed6", label: "1 000 – 3 000" },
          { color: "#9ecae1", label: "500 – 1 000" },
          { color: "#c6dbef", label: "100 – 500" },
          { color: "#deebf7", label: "< 100" },
        ];
      } else if (this.activeCategory === 3) {
        this.legendItems = [
          { color: "#08306b", label: "> 20 km²" },
          { color: "#2171b5", label: "10 – 20 km²" },
          { color: "#4292c6", label: "5 – 10 km²" },
          { color: "#6baed6", label: "3 – 5 km²" },
          { color: "#9ecae1", label: "1 – 3 km²" },
          { color: "#c6dbef", label: "0.5 – 1 km²" },
          { color: "#deebf7", label: "< 0.5 km²" },
        ];
      } else if (isAge) {
        this.legendItems = [
          { color: "#08306b", label: "> 4 000" },
          { color: "#2171b5", label: "3 000 – 4 000" },
          { color: "#4292c6", label: "2 000 – 3 000" },
          { color: "#6baed6", label: "1 000 – 2 000" },
          { color: "#9ecae1", label: "500 – 1 000" },
          { color: "#c6dbef", label: "100 – 500" },
          { color: "#deebf7", label: "< 100" },
        ];
      } else if (isGender) {
        this.legendItems = [
          { color: "#08306b", label: "> 15 000" },
          { color: "#2171b5", label: "10 000 – 15 000" },
          { color: "#4292c6", label: "7 500 – 10 000" },
          { color: "#6baed6", label: "5 000 – 7 500" },
          { color: "#9ecae1", label: "2 500 – 5 000" },
          { color: "#c6dbef", label: "500 – 2 500" },
          { color: "#deebf7", label: "< 500" },
        ];
      } else {
        this.legendItems = [
          { color: "#08306b", label: "> 30 000" },
          { color: "#2171b5", label: "20 000 – 30 000" },
          { color: "#4292c6", label: "15 000 – 20 000" },
          { color: "#6baed6", label: "10 000 – 15 000" },
          { color: "#9ecae1", label: "5 000 – 10 000" },
          { color: "#c6dbef", label: "1 000 – 5 000" },
          { color: "#deebf7", label: "< 1 000" },
        ];
      }
    },

    formatNumber(num) {
      if (num === undefined || num === null) return "0";
      return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    },

    calculateDensityByDemography(props) {
      if (!props.powierzchnia || props.powierzchnia === 0) {
        return 0;
      }
      const pop = this.getPopulationByDemography(props);
      return pop / props.powierzchnia;
    },
  },

  computed: {
    dostepneKategorie() {
      if (this.noweZdarzenie.kategoria2 === "zgloszenie") {
        return this.zgloszenieKategorie;
      } else if (this.noweZdarzenie.kategoria2 === "wydarzenie") {
        return this.wydarzenieKategorie;
      }
      return [];
    },

    wszystkieKategorie() {
      return [...this.zgloszenieKategorie, ...this.wydarzenieKategorie];
    },

    dzielnicaStats() {
      if (!this.hoveredDzielnicaSpolecznosc || !this.zdarzeniaData) {
        return { total: 0, zgloszenia: 0, wydarzenia: 0 };
      }

      const dzielnicaNazwa = this.hoveredDzielnicaSpolecznosc;
      const features = this.zdarzeniaData.features || [];

      let zgloszenia = 0;
      let wydarzenia = 0;

      features.forEach((f) => {
        if (f.properties.dzielnica === dzielnicaNazwa) {
          if (f.properties.kategoria2 === "zgloszenie") {
            zgloszenia++;
          } else if (f.properties.kategoria2 === "wydarzenie") {
            wydarzenia++;
          }
        }
      });

      return {
        total: zgloszenia + wydarzenia,
        zgloszenia,
        wydarzenia,
      };
    },

    dzielnicaRanking() {
      if (!this.dzielnicaData || !this.zdarzeniaData) return [];

      const stats = {};

      this.dzielnicaData.features.forEach((f) => {
        const nazwa = f.properties.nazwa;
        stats[nazwa] = { nazwa, total: 0, zgloszenia: 0, wydarzenia: 0 };
      });

      this.zdarzeniaData.features.forEach((f) => {
        const dzielnica = f.properties.dzielnica;
        if (dzielnica && stats[dzielnica]) {
          if (f.properties.kategoria2 === "zgloszenie") {
            stats[dzielnica].zgloszenia++;
            stats[dzielnica].total++;
          } else if (f.properties.kategoria2 === "wydarzenie") {
            stats[dzielnica].wydarzenia++;
            stats[dzielnica].total++;
          }
        }
      });

      const sortKey = this.rankingSort;
      return Object.values(stats)
        .map((item) => ({
          nazwa: item.nazwa,
          count:
            sortKey === "total"
              ? item.total
              : sortKey === "zgloszenia"
              ? item.zgloszenia
              : item.wydarzenia,
        }))
        .sort((a, b) => b.count - a.count);
    },

    wazneMiejscaStats() {
      if (!this.hoveredDzielnicaWazneMiejsca) {
        return { total: 0, szkoly: 0, apteki: 0 };
      }

      const dzielnicaNazwa = this.hoveredDzielnicaWazneMiejsca;

      const szkoly = this.szkolyData.filter(
        (s) => s.dzielnica === dzielnicaNazwa
      ).length;
      const apteki = this.aptekiData.filter(
        (a) => a.dzielnica === dzielnicaNazwa
      ).length;

      return {
        total: szkoly + apteki,
        szkoly,
        apteki,
      };
    },

    wazneMiejscaRanking() {
      if (!this.dzielnicaData) return [];

      const stats = {};

      this.dzielnicaData.features.forEach((f) => {
        const nazwa = f.properties.nazwa;
        stats[nazwa] = { nazwa, total: 0, szkoly: 0, apteki: 0 };
      });

      this.szkolyData.forEach((item) => {
        if (item.dzielnica && stats[item.dzielnica]) {
          stats[item.dzielnica].szkoly++;
          stats[item.dzielnica].total++;
        }
      });

      this.aptekiData.forEach((item) => {
        if (item.dzielnica && stats[item.dzielnica]) {
          stats[item.dzielnica].apteki++;
          stats[item.dzielnica].total++;
        }
      });

      const sortKey = this.wazneMiejscaRankingSort;
      return Object.values(stats)
        .map((item) => ({
          nazwa: item.nazwa,
          count:
            sortKey === "total"
              ? item.total
              : sortKey === "szkoly"
              ? item.szkoly
              : item.apteki,
        }))
        .sort((a, b) => b.count - a.count);
    },

    currentDemographyLabel() {
      const ageLabels = {
        all: "",
        mlodzi: " (młodzi)",
        dorosli: " (dorośli)",
        seniorzy: " (seniorzy)",
      };
      const ageSuffix = ageLabels[this.selectedAge] || "";

      if (this.selectedDemography === "kobiety")
        return "Liczba kobiet" + ageSuffix;
      if (this.selectedDemography === "mezczyzni")
        return "Liczba mężczyzn" + ageSuffix;
      return "Liczba mieszkańców" + ageSuffix;
    },

    legendTitle() {
      if (this.activeCategory === 2) return "Gęstość (os/km²)";
      if (this.activeCategory === 3) return "Powierzchnia";
      return this.currentDemographyLabel;
    },

    currentColorFunction() {
      const self = this;
      const isGender = this.selectedDemography !== "all";
      const isAge = this.selectedAge !== "all";

      if (this.activeCategory === 2) {
        return (val) => {
          return val > 10000
            ? "#08306b"
            : val > 5000
            ? "#2171b5"
            : val > 3000
            ? "#4292c6"
            : val > 1000
            ? "#6baed6"
            : val > 500
            ? "#9ecae1"
            : val > 100
            ? "#c6dbef"
            : "#deebf7";
        };
      } else if (this.activeCategory === 3) {
        return (val) => {
          return val > 20
            ? "#08306b"
            : val > 10
            ? "#2171b5"
            : val > 5
            ? "#4292c6"
            : val > 3
            ? "#6baed6"
            : val > 1
            ? "#9ecae1"
            : val > 0.5
            ? "#c6dbef"
            : "#deebf7";
        };
      } else if (isAge) {
        return self.getColorForAgeGroup;
      } else if (isGender) {
        return self.getColorForGender;
      }
      return self.getColorForPopulation;
    },
  },

  watch: {
    spolecznoscFilter() {
      if (this.activeSection === "spolecznosc") {
        this.displayZdarzenia();

        if (this.heatmapEnabled) {
          this.showHeatmap();
        }
      }
    },
    wazneMiejscaFilter() {
      if (this.activeSection === "zdrowie") {
        this.displayWazneMiejsca();
        if (this.wazneMiejscaHeatmap) {
          this.showWazneMiejscaHeatmap();
        }
      }
    },
  },
};
</script>

<style>
:root {
  --white: #ffffff;
  --pink: #e56a80;
  --cherry: #c21938;
  --burgundy: #780f22;
  --black: #000000;
  --gray-light: #f5f5f5;
  --gray: #e0e0e0;
  --gray-dark: #666;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body, .app {
  height: 100%;
  width: 100%;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.app {
  display: flex;
  flex-direction: column;
}

/* Top Navigation Bar */
.topbar {
  display: flex;
  align-items: center;
  background: var(--black);
  padding: 0 20px;
  height: 56px;
  gap: 20px;
  position: relative;
  z-index: 2000;
}

.topbar-brand {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.logo {
  width: 4vw;
}



.topbar-subtitle {
  color: var(--pink);
  font-size: 12px;
}

.topbar-nav {
  display: flex;
  gap: 4px;
  flex: 1;
}

.nav-btn {
  padding: 8px 16px;
  border: none;
  background: transparent;
  color: var(--white);
  cursor: pointer;
  font-size: 13px;
  border-radius: 4px;
  transition: background 0.2s;
}

.nav-btn:hover {
  background: var(--burgundy);
}

.nav-btn.active {
  background: var(--cherry);
}

.nav-btn-admin {
  color: var(--pink);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.login-btn {
  padding: 6px 14px;
  border: 1px solid var(--pink);
  background: transparent;
  color: var(--pink);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.login-btn:hover {
  background: var(--pink);
  color: var(--white);
}

.admin-badge {
  padding: 4px 10px;
  background: var(--cherry);
  color: var(--white);
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
  cursor: pointer;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
}

.mobile-menu-btn span {
  display: block;
  width: 20px;
  height: 2px;
  background: var(--white);
}

.mobile-menu {
  display: none;
  position: absolute;
  top: 56px;
  left: 0;
  right: 0;
  background: var(--black);
  flex-direction: column;
  z-index: 1999;
}

.mobile-nav-btn {
  padding: 14px 20px;
  border: none;
  background: transparent;
  color: var(--white);
  text-align: left;
  cursor: pointer;
  font-size: 14px;
  border-bottom: 1px solid var(--burgundy);
}

.mobile-nav-btn.active {
  background: var(--cherry);
}

/* Main content */
.main-content {
  flex: 1;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
}

/* Section panel */
.section-panel {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--white);
  padding: 16px;
  border-radius: 6px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  max-width: 360px;
}

.section-panel h3 {
  margin-bottom: 12px;
  color: var(--black);
  font-size: 15px;
  font-weight: 600;
  border-bottom: 2px solid var(--cherry);
  padding-bottom: 8px;
}

.section-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-group span {
  font-weight: 500;
  color: var(--gray-dark);
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.filter-btn {
  padding: 6px 12px;
  border: 1px solid var(--gray);
  background: var(--white);
  color: var(--black);
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: var(--cherry);
  color: var(--cherry);
}

.filter-btn.active {
  background: var(--cherry);
  border-color: var(--cherry);
  color: var(--white);
}

.filter-btn.heatmap-btn {
  border-color: var(--pink);
  color: var(--pink);
}

.filter-btn.heatmap-btn.active {
  background: var(--pink);
  color: var(--white);
}

/* Info panel */
.info-panel {
  position: absolute;
  top: 10px;
  right: 10px;
  background: var(--white);
  padding: 14px;
  border-radius: 6px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  min-width: 180px;
}

.info-panel h3 {
  margin-bottom: 10px;
  color: var(--black);
  font-size: 14px;
  font-weight: 600;
  border-bottom: 2px solid var(--cherry);
  padding-bottom: 6px;
}

.info-panel p {
  margin: 4px 0;
  font-size: 12px;
  color: var(--gray-dark);
}

.info-panel hr {
  border: none;
  border-top: 1px solid var(--gray);
  margin: 8px 0;
}

.info-hint {
  opacity: 0.8;
}

.info-hint p {
  font-style: italic;
  color: var(--gray-dark);
}

/* Legend */
.legend {
  position: absolute;
  bottom: 20px;
  right: 10px;
  background: var(--white);
  padding: 12px;
  border-radius: 6px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

.legend h4 {
  margin-bottom: 8px;
  color: var(--black);
  font-size: 12px;
  font-weight: 600;
}

.legend-item {
  display: flex;
  align-items: center;
  margin: 3px 0;
}

.legend-color {
  width: 16px;
  height: 12px;
  margin-right: 6px;
  border: 1px solid var(--gray);
}

.legend-label {
  font-size: 11px;
  color: var(--gray-dark);
}

/* Form panel */
.form-panel {
  max-width: 280px;
}

.zdarzenie-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.form-group label {
  font-weight: 500;
  font-size: 11px;
  color: var(--gray-dark);
  text-transform: uppercase;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 8px 10px;
  border: 1px solid var(--gray);
  border-radius: 4px;
  font-size: 13px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--cherry);
}

.form-group textarea {
  resize: vertical;
}

.location-display {
  padding: 8px;
  background: var(--gray-light);
  border-radius: 4px;
  font-size: 11px;
  color: var(--black);
  border-left: 3px solid var(--cherry);
}

.location-hint {
  padding: 8px;
  background: var(--gray-light);
  border-radius: 4px;
  font-size: 11px;
  color: var(--gray-dark);
}

.location-error {
  padding: 8px;
  background: #fff0f0;
  border-radius: 4px;
  font-size: 11px;
  color: var(--cherry);
  border: 1px solid var(--pink);
}

/* Panel statystyk dzielnicy */
.dzielnica-stats-panel {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--white);
  padding: 12px 20px;
  border-radius: 6px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  min-width: 260px;
  text-align: center;
}

.dzielnica-stats-panel h4 {
  margin: 0 0 10px 0;
  color: var(--black);
  font-size: 14px;
  font-weight: 600;
}

.dzielnica-stats-panel.stats-hint {
  opacity: 0.7;
  min-width: 200px;
}

.dzielnica-stats-panel.stats-hint p {
  margin: 0;
  color: var(--gray-dark);
  font-size: 12px;
}

.stats-grid {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 14px;
  border-radius: 4px;
  min-width: 70px;
  background: var(--gray-light);
}

.stat-number {
  font-size: 20px;
  font-weight: 700;
  color: var(--cherry);
}

.stat-label {
  font-size: 10px;
  color: var(--gray-dark);
  text-transform: uppercase;
}

/* Panel rankingu dzielnic */
.dzielnice-ranking-panel {
  position: absolute;
  bottom: 20px;
  left: 10px;
  background: var(--white);
  padding: 12px;
  border-radius: 6px;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
  width: 200px;
  max-height: 300px;
  display: flex;
  flex-direction: column;
}

.dzielnice-ranking-panel h4 {
  margin: 0 0 8px 0;
  color: var(--black);
  font-size: 12px;
  font-weight: 600;
}

.ranking-filters {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}

.ranking-filter-btn {
  flex: 1;
  padding: 4px;
  border: 1px solid var(--gray);
  background: var(--white);
  border-radius: 3px;
  font-size: 10px;
  cursor: pointer;
}

.ranking-filter-btn.active {
  background: var(--cherry);
  color: var(--white);
  border-color: var(--cherry);
}

.ranking-list {
  overflow-y: auto;
  flex: 1;
}

.ranking-item {
  display: flex;
  align-items: center;
  padding: 5px 6px;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 2px;
}

.ranking-item:hover {
  background: var(--gray-light);
}

.ranking-position {
  width: 18px;
  height: 18px;
  background: var(--gray-light);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 9px;
  font-weight: 600;
  color: var(--gray-dark);
  margin-right: 6px;
}

.ranking-item.has-events .ranking-position {
  background: var(--cherry);
  color: var(--white);
}

.ranking-name {
  flex: 1;
  font-size: 11px;
  color: var(--black);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ranking-count {
  font-size: 12px;
  font-weight: 600;
  color: var(--cherry);
  min-width: 20px;
  text-align: right;
}

/* Panel komentarzy */
.komentarze-panel {
  position: absolute;
  bottom: 20px;
  right: 10px;
  background: var(--white);
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  width: 280px;
  max-height: 380px;
  display: flex;
  flex-direction: column;
  z-index: 1001;
  overflow: hidden;
}

.komentarze-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 12px;
  background: var(--black);
  color: var(--white);
}

.komentarze-header h4 {
  margin: 0;
  font-size: 13px;
}

.close-btn {
  background: none;
  border: none;
  color: var(--white);
  font-size: 16px;
  cursor: pointer;
}

.komentarze-zdarzenie-info {
  padding: 8px 12px;
  background: var(--gray-light);
  border-bottom: 1px solid var(--gray);
}

.komentarze-zdarzenie-info strong {
  display: block;
  font-size: 12px;
  color: var(--black);
}

.zdarzenie-type {
  font-size: 10px;
  color: var(--cherry);
}

.komentarze-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px;
  max-height: 180px;
}

.komentarz-item {
  background: var(--gray-light);
  border-radius: 4px;
  padding: 8px;
  margin-bottom: 6px;
}

.komentarz-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
}

.komentarz-autor {
  font-weight: 600;
  font-size: 11px;
  color: var(--cherry);
}

.komentarz-data {
  font-size: 9px;
  color: var(--gray-dark);
}

.komentarz-tresc {
  margin: 0;
  font-size: 12px;
  color: var(--black);
  line-height: 1.4;
}

.komentarze-empty {
  padding: 16px 12px;
  text-align: center;
}

.komentarze-empty p {
  margin: 0;
  color: var(--gray-dark);
  font-size: 12px;
}

.komentarz-form {
  padding: 10px 12px;
  border-top: 1px solid var(--gray);
  background: var(--gray-light);
}

.komentarz-input {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--gray);
  border-radius: 4px;
  font-size: 12px;
  margin-bottom: 6px;
}

.komentarz-input:focus {
  outline: none;
  border-color: var(--cherry);
}

.tresc-input {
  resize: none;
}

.submit-komentarz-btn {
  width: 100%;
  padding: 8px;
  background: var(--cherry);
  color: var(--white);
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.submit-komentarz-btn:hover {
  background: #2980b9;
}

.submit-komentarz-btn:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.submit-btn {
  padding: 10px;
  background: #3498db;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.submit-btn:hover {
  background: var(--burgundy);
}

.submit-btn:disabled {
  background: var(--gray);
  cursor: not-allowed;
}

.form-message {
  padding: 8px;
  background: var(--gray-light);
  border-radius: 4px;
  font-size: 11px;
  color: var(--black);
  text-align: center;
  border-left: 3px solid var(--cherry);
}

/* Vote buttons */
.vote-btn {
  padding: 4px 8px;
  border: 1px solid var(--gray);
  border-radius: 4px;
  background: var(--white);
  cursor: pointer;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.vote-btn:hover:not(:disabled) {
  border-color: var(--cherry);
}

.vote-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Modal */
.age-modal-overlay,
.admin-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}

.age-modal,
.admin-modal {
  background: var(--white);
  border-radius: 8px;
  width: 340px;
  max-width: 90%;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  overflow: hidden;
}

.age-modal-header,
.admin-modal-header {
  background: var(--black);
  padding: 16px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.logo_header {
  width: 7vw;
}



.age-modal-content,
.admin-modal-content {
  padding: 20px;
}

.age-modal-content p,
.admin-modal-content p {
  color: var(--gray-dark);
  margin: 0 0 16px 0;
  font-size: 13px;
  line-height: 1.5;
}

.age-input-group,
.admin-input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.age-input-group label,
.admin-input-group label {
  color: var(--black);
  font-size: 12px;
  font-weight: 500;
}

.age-input-group input,
.admin-input-group input {
  padding: 10px 12px;
  border: 1px solid var(--gray);
  border-radius: 4px;
  background: var(--white);
  color: var(--black);
  font-size: 14px;
  text-align: center;
}

.age-input-group input:focus,
.admin-input-group input:focus {
  outline: none;
  border-color: var(--cherry);
}

.age-modal-footer,
.admin-modal-footer {
  padding: 0 20px 20px;
}

.age-confirm-btn,
.admin-login-btn {
  width: 100%;
  padding: 12px;
  background: var(--cherry);
  color: var(--white);
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.age-confirm-btn:hover:not(:disabled),
.admin-login-btn:hover:not(:disabled) {
  background: var(--burgundy);
}

.age-confirm-btn:disabled,
.admin-login-btn:disabled {
  background: var(--gray);
  cursor: not-allowed;
}

.admin-error {
  margin-top: 10px;
  padding: 8px;
  background: #fff0f0;
  border-radius: 4px;
  color: var(--cherry);
  font-size: 12px;
}

.close-modal-btn {
  background: none;
  border: none;
  color: var(--white);
  font-size: 18px;
  cursor: pointer;
}

/* Checkbox */
.checkbox-group {
  margin-top: 8px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 8px 10px;
  background: var(--gray-light);
  border-radius: 4px;
}

.checkbox-label:hover {
  background: rgba(52, 152, 219, 0.15);
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
  accent-color: #3498db;
}

.checkbox-text {
  font-size: 12px;
  color: var(--black);
}



/* Admin panel simplified */
.admin-info-box {
  background: var(--gray-light);
  border-radius: 4px;
  padding: 12px;
  margin-bottom: 10px;
}

.admin-info-box h4 {
  margin: 0 0 8px 0;
  color: var(--black);
  font-size: 12px;
  font-weight: 600;
}

.admin-info-box p {
  margin: 0 0 8px 0;
  color: var(--gray-dark);
  font-size: 12px;
}

.admin-stats {
  display: flex;
  gap: 10px;
}

.admin-stat-item {
  flex: 1;
  text-align: center;
  padding: 10px;
  background: var(--white);
  border-radius: 4px;
  border: 1px solid var(--gray);
}

.admin-stat-item .stat-value {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: var(--cherry);
}

.admin-stat-item .stat-desc {
  display: block;
  font-size: 10px;
  color: var(--gray-dark);
  margin-top: 2px;
}

.admin-hidden-list {
  margin: 0;
  padding-left: 16px;
  color: var(--gray-dark);
  font-size: 11px;
}

.admin-hidden-list li {
  margin: 4px 0;
}

.admin-actions {
  display: flex;
  gap: 8px;
}

.admin-action-btn {
  flex: 1;
  padding: 8px 12px;
  background: var(--cherry);
  color: var(--white);
  border: none;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.admin-action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
}

/* Admin indicator */
.admin-indicator {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #f1c40f 0%, #f39c12 100%);
  color: #1a1a2e;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(241, 196, 15, 0.4);
}

/* Panel propozycji działań */
.proposal-panel {
  max-width: 320px;
  max-height: 500px;
  overflow-y: auto;
  border: 2px solid rgba(241, 196, 15, 0.3);
  margin-top: 10px;
  margin-right: 14vw;
}

.proposal-panel h3 {
  color: #f39c12;
  border-bottom-color: #f39c12;
}

.proposal-description {
  font-size: 12px;
  color: #7f8c8d;
  margin-bottom: 12px;
}

.generate-btn {
  width: 100%;
  padding: 12px 16px;
  background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 15px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(243, 156, 18, 0.4);
}

.generate-btn:disabled {
  background: #95a5a6;
  cursor: wait;
}

.proposals-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.proposal-item {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 12px;
  border-left: 4px solid #3498db;
  transition: all 0.2s ease;
}

.proposal-item:hover {
  transform: translateX(3px);
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
}

.proposal-item.intervention {
  border-left-color: #e74c3c;
  background: linear-gradient(135deg, #fff5f5 0%, #fff 100%);
}

.proposal-item.event {
  border-left-color: #9b59b6;
  background: linear-gradient(135deg, #faf5ff 0%, #fff 100%);
}

.proposal-item.investment {
  border-left-color: #3498db;
  background: linear-gradient(135deg, #f0f9ff 0%, #fff 100%);
}

.proposal-item.social {
  border-left-color: #e67e22;
  background: linear-gradient(135deg, #fffaf0 0%, #fff 100%);
}

.proposal-item.info {
  border-left-color: #95a5a6;
  background: linear-gradient(135deg, #f8f9fa 0%, #fff 100%);
}

.proposal-item.success {
  border-left-color: #27ae60;
  background: linear-gradient(135deg, #f0fff4 0%, #fff 100%);
}

.proposal-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.proposal-icon {
  font-size: 18px;
}

.proposal-type-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
  text-transform: uppercase;
}

.proposal-type-badge.intervention {
  background: #ffebee;
  color: #c0392b;
}

.proposal-type-badge.event {
  background: #f3e5f5;
  color: #7b1fa2;
}

.proposal-type-badge.investment {
  background: #e3f2fd;
  color: #1565c0;
}

.proposal-type-badge.social {
  background: #fff3e0;
  color: #e65100;
}

.proposal-type-badge.info {
  background: #eceff1;
  color: #546e7a;
}

.proposal-type-badge.success {
  background: #e8f5e9;
  color: #2e7d32;
}

.proposal-title {
  margin: 0 0 6px 0;
  font-size: 13px;
  color: #2c3e50;
  font-weight: 600;
}

.proposal-desc {
  margin: 0 0 8px 0;
  font-size: 12px;
  color: #555;
  line-height: 1.4;
}

.proposal-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 11px;
}

.proposal-location {
  color: #7f8c8d;
}

.proposal-priority {
  font-weight: 600;
}

.proposal-priority.high {
  color: #e74c3c;
}

.proposal-priority.medium {
  color: #f39c12;
}

.proposal-priority.low {
  color: #27ae60;
}

.proposals-empty {
  text-align: center;
  padding: 20px;
  color: #95a5a6;
}

.proposals-empty p {
  margin: 0;
  font-size: 13px;
  font-style: italic;
}

/* Panel analizy infrastruktury */
.analysis-panel {
  max-width: 340px;
  max-height: 520px;
  overflow-y: auto;
  border: 2px solid rgba(155, 89, 182, 0.3);
  margin-top: 10px;
}

.analysis-panel h3 {
  color: #9b59b6;
  border-bottom-color: #9b59b6;
}

.analysis-description {
  font-size: 12px;
  color: #7f8c8d;
  margin-bottom: 12px;
}

.analysis-results {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 15px;
}

.analysis-item {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 12px;
  border-left: 4px solid #9b59b6;
}

.analysis-item.szkola {
  border-left-color: #3498db;
  background: linear-gradient(135deg, #f0f9ff 0%, #fff 100%);
}

.analysis-item.apteka {
  border-left-color: #27ae60;
  background: linear-gradient(135deg, #f0fff4 0%, #fff 100%);
}

/* Styl dla osiedli BEZ żadnej infrastruktury - najwyższy priorytet */
.analysis-item.extreme {
  border-left-color: #000 !important;
  border-left-width: 6px;
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%) !important;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.analysis-item.extreme .analysis-dzielnica,
.analysis-item.extreme .analysis-desc,
.analysis-item.extreme .analysis-stats {
  color: #fff !important;
}

.analysis-item.extreme .analysis-stats .ratio {
  color: #e74c3c !important;
  font-weight: bold;
}

.analysis-item.extreme .simulate-btn {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  animation: pulse-btn 1.5s ease-in-out infinite;
}

@keyframes pulse-btn {
  0%, 100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
  50% { box-shadow: 0 0 0 10px rgba(231, 76, 60, 0); }
}

.analysis-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.analysis-icon {
  font-size: 20px;
}

.analysis-dzielnica {
  flex: 1;
  font-weight: 600;
  color: #2c3e50;
  font-size: 13px;
}

.analysis-severity {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 600;
}

.analysis-severity.extreme {
  background: #000;
  color: #fff;
  animation: pulse-extreme 1s ease-in-out infinite;
}

@keyframes pulse-extreme {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}

.analysis-severity.critical {
  background: #ffebee;
  color: #c0392b;
}

.analysis-severity.warning {
  background: #fff3e0;
  color: #e65100;
}

/* Styl dla elementów z extreme severity */
.analysis-item.extreme-priority {
  border-left-width: 6px;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);
}

.analysis-desc {
  margin: 0 0 10px 0;
  font-size: 12px;
  color: #555;
  line-height: 1.4;
}

.analysis-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  font-size: 11px;
  color: #7f8c8d;
  margin-bottom: 10px;
}

.analysis-stats .ratio {
  color: #e67e22;
  font-weight: 600;
}

.simulate-btn {
  width: 100%;
  padding: 8px 12px;
  background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.simulate-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(155, 89, 182, 0.4);
}

.analysis-empty {
  text-align: center;
  padding: 20px;
  background: #e8f5e9;
  border-radius: 10px;
  margin-top: 15px;
}

.analysis-empty p {
  margin: 0;
  color: #27ae60;
  font-size: 13px;
}

/* Symulowane miejsca */
.simulated-places {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.simulated-places h4 {
  margin: 0 0 12px 0;
  font-size: 13px;
  color: #e67e22;
}

.simulated-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  background: linear-gradient(135deg, #fff5eb 0%, #fff 100%);
  border: 1px solid rgba(230, 126, 34, 0.2);
  border-radius: 8px;
  margin-bottom: 8px;
}

.simulated-icon {
  font-size: 16px;
}

.simulated-name {
  flex: 1;
  font-size: 12px;
  font-weight: 500;
  color: #2c3e50;
}

.simulated-location {
  font-size: 10px;
  color: #7f8c8d;
}

.remove-simulated-btn {
  background: none;
  border: none;
  color: #e74c3c;
  cursor: pointer;
  font-size: 14px;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}

.remove-simulated-btn:hover {
  background: #ffebee;
}

.clear-simulations-btn {
  width: 100%;
  padding: 8px;
  background: #fff;
  border: 1px solid #e74c3c;
  color: #e74c3c;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  margin-top: 8px;
  transition: all 0.2s;
}

.clear-simulations-btn:hover {
  background: #ffebee;
}

/* Symulowane markery na mapie */
.simulated-marker-container {
  background: transparent !important;
  border: none !important;
}

.simulated-marker {
  position: relative;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.simulated-marker .marker-icon {
  font-size: 24px;
  z-index: 2;
  position: relative;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.simulated-marker .marker-pulse {
  position: absolute;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(230, 126, 34, 0.4);
  animation: pulse-animation 1.5s ease-out infinite;
}

.simulated-marker.szkola .marker-pulse {
  background: rgba(52, 152, 219, 0.4);
}

.simulated-marker.apteka .marker-pulse {
  background: rgba(39, 174, 96, 0.4);
}

@keyframes pulse-animation {
  0% {
    transform: scale(0.5);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

/* Admin indicator */
.admin-indicator {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--cherry);
  color: var(--white);
  padding: 6px 14px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 500;
  z-index: 1000;
}

/* Simplified panels */
.proposal-panel,
.analysis-panel,
.admin-panel {
  max-width: 300px;
  border-left: 3px solid var(--cherry);
}

.proposal-panel h3,
.analysis-panel h3,
.admin-panel h3 {
  color: var(--cherry);
}

.generate-btn {
  width: 100%;
  padding: 10px;
  background: var(--cherry);
  color: var(--white);
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  margin-bottom: 12px;
}

.generate-btn:hover:not(:disabled) {
  background: var(--burgundy);
}

.generate-btn:disabled {
  background: var(--gray);
}

.proposals-list,
.analysis-results {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.proposal-item,
.analysis-item {
  background: var(--gray-light);
  border-radius: 4px;
  padding: 10px;
  border-left: 3px solid var(--cherry);
}

.proposal-title,
.analysis-dzielnica {
  font-size: 12px;
  font-weight: 600;
  color: var(--black);
  margin-bottom: 4px;
}

.proposal-desc,
.analysis-desc {
  font-size: 11px;
  color: var(--gray-dark);
  margin: 0;
  line-height: 1.4;
}

.simulate-btn {
  width: 100%;
  padding: 6px;
  background: var(--cherry);
  color: var(--white);
  border: none;
  border-radius: 4px;
  font-size: 11px;
  cursor: pointer;
  margin-top: 8px;
}

.simulate-btn:hover {
  background: var(--burgundy);
}

/* Responsive */
@media (max-width: 768px) {
  .topbar-nav {
    display: none;
  }
  
  .topbar-actions {
    display: none;
  }
  
  .mobile-menu-btn {
    display: flex;
  }
  
  .mobile-menu {
    display: flex;
  }
  
  .section-panel {
    left: 5px;
    right: 5px;
    max-width: none;
    top: 5px;
  }
  
  .info-panel {
    right: 5px;
    left: 5px;
    max-width: none;
  }
  
  .dzielnice-ranking-panel {
    width: calc(100% - 10px);
    left: 5px;
    bottom: 10px;
    max-height: 200px;
  }
  
  .dzielnica-stats-panel {
    width: calc(100% - 20px);
    min-width: auto;
  }
  
  .komentarze-panel {
    width: calc(100% - 10px);
    right: 5px;
    max-height: 300px;
  }
  
  .legend {
    bottom: 10px;
    right: 5px;
  }
  
  .proposal-panel,
  .analysis-panel {
    max-width: none;
  }
}

@media (max-width: 480px) {
  .topbar {
    padding: 0 12px;
  }
  
  .topbar-brand h1 {
    font-size: 18px;
  }
  
  .section-panel,
  .info-panel {
    padding: 10px;
  }
  
  .filter-btn {
    padding: 5px 8px;
    font-size: 11px;
  }
}
</style>
