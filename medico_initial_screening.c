#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <time.h>

typedef struct {
    char name[80];
    int age;
    char gender[16];
    char contact[32];
    char arrivalTime[32];
} Patient;

typedef struct {
    float temperatureC;
    int heartRate;
    int systolicBP;
    int diastolicBP;
    int spo2;
} Vitals;

typedef struct {
    bool unconscious;
    bool severeBleeding;
    bool chestPain;
    bool breathingDifficulty;
    bool strokeSigns;
    bool seizureNow;
    bool highFever;
    bool fractureOrMajorTrauma;
    bool persistentVomiting;
    bool dehydration;
    bool coughCold;
    bool abdominalPainSevere;
    bool pregnancyComplication;
} Symptoms;

// Utility function to safely get string input
void getString(const char *prompt, char *buffer, size_t size) {
    printf("%s", prompt);
    if (fgets(buffer, size, stdin)) {
        buffer[strcspn(buffer, "\n")] = 0; 
    }
}

int getInt(const char *prompt) {
    char buffer[32];
    int value;
    while (1) {
        printf("%s", prompt);
        if (fgets(buffer, sizeof(buffer), stdin)) {
            if (sscanf(buffer, "%d", &value) == 1) {
                return value;
            }
        }
        printf("Invalid input. Please enter a valid number.\n");
    }
}

float getFloat(const char *prompt) {
    char buffer[32];
    float value;
    while (1) {
        printf("%s", prompt);
        if (fgets(buffer, sizeof(buffer), stdin)) {
            if (sscanf(buffer, "%f", &value) == 1) {
                return value;
            }
        }
        printf("Invalid input. Please enter a valid number.\n");
    }
}

bool yn(const char *label) {
    char ans[8];
    while (1) {
        printf("%s (y/n): ", label);
        if (fgets(ans, sizeof(ans), stdin)) {
            char c = tolower(ans[0]);
            if (c == 'y') return true;
            if (c == 'n') return false;
        }
        printf("Invalid input. Please enter y or n.\n");
    }
}

void inputPatient(Patient *p) {
    printf("=== Patient Details ===\n");
    getString("Full name: ", p->name, sizeof(p->name));
    p->age = getInt("Age (years): ");
    getString("Gender: ", p->gender, sizeof(p->gender));
    getString("Contact number: ", p->contact, sizeof(p->contact));
    getString("Arrival time (e.g., 10:25 AM): ", p->arrivalTime, sizeof(p->arrivalTime));
}

void inputVitals(Vitals *v) {
    printf("\n=== Vitals ===\n");
    v->temperatureC = getFloat("Temperature (C): ");
    v->heartRate = getInt("Heart rate (bpm): ");
    v->systolicBP = getInt("Systolic BP (mmHg): ");
    v->diastolicBP = getInt("Diastolic BP (mmHg): ");
    v->spo2 = getInt("SpO2 (%): ");
}

void inputSymptoms(Symptoms *s) {
    printf("\n=== Symptoms / Complaints ===\n");
    s->unconscious           = yn("Unconscious or not fully responsive");
    s->severeBleeding        = yn("Severe bleeding");
    s->chestPain             = yn("Chest pain/pressure");
    s->breathingDifficulty   = yn("Difficulty breathing/shortness of breath");
    s->strokeSigns           = yn("Stroke signs (face droop/arm weakness/speech trouble)");
    s->seizureNow            = yn("Seizure now or very recent");
    s->highFever             = yn("High fever");
    s->fractureOrMajorTrauma = yn("Suspected fracture or major trauma");
    s->persistentVomiting    = yn("Persistent vomiting");
    s->dehydration           = yn("Signs of dehydration");
    s->coughCold             = yn("Cough/cold-like illness");
    s->abdominalPainSevere   = yn("Severe abdominal pain");
    s->pregnancyComplication = yn("Pregnancy with bleeding/severe pain");
}

bool isEmergency(const Patient *p, const Vitals *v, const Symptoms *s) {
    if (s->unconscious || s->severeBleeding || s->strokeSigns || s->seizureNow)
        return true;
    if (s->breathingDifficulty || v->spo2 < 92)
        return true;
    if (s->chestPain && (p->age >= 40 || v->spo2 < 94))
        return true;
    if (s->fractureOrMajorTrauma)
        return true;
    if (s->pregnancyComplication)
        return true;
    if (v->temperatureC >= 40.0 || v->temperatureC < 35.0)
        return true;
    if (v->heartRate > 130 || v->heartRate < 40)
        return true;
    if (v->systolicBP > 180 || v->systolicBP < 80)
        return true;
    if (s->highFever && p->age < 3)
        return true;
    if (s->abdominalPainSevere && (v->systolicBP < 90 || v->spo2 < 94))
        return true;
    return false;
}

const char* allocateDoctor(const Patient *p, const Vitals *v, const Symptoms *s, bool emergency) {
    (void)v;
    if (emergency) return "Emergency Medicine (ER)";
    if (p->age < 14) return "Pediatrics";
    if (s->chestPain) return "Cardiology";
    if (s->breathingDifficulty || s->coughCold) return "Pulmonology / Respiratory";
    if (s->strokeSigns || s->seizureNow) return "Neurology";
    if (s->fractureOrMajorTrauma) return "Orthopedics";
    if (s->abdominalPainSevere || s->persistentVomiting) return "General Surgery / Gastroenterology";
    if (s->pregnancyComplication) return "Obstetrics & Gynecology";
    if (s->dehydration || s->highFever) return "General Medicine";
    return "General Medicine";
}

void printPrecautions(FILE *fp, const Patient *p, const Vitals *v, const Symptoms *s, bool emergency) {
    fprintf(fp, "\n--- Precautions ---\n");
    if (emergency) {
        fprintf(fp, "* Keep patient under observation; no food/drink unless advised.\n");
        fprintf(fp, "* Ensure airway is clear; sit upright if breathing difficulty.\n");
        fprintf(fp, "* If bleeding: apply firm pressure with clean cloth.\n");
    }
    if (s->chestPain) fprintf(fp, "* Rest; limit movement; loosen tight clothing.\n");
    if (s->breathingDifficulty || v->spo2 < 94 || s->coughCold) fprintf(fp, "* Sit upright; encourage steady breaths; wear mask if coughing.\n");
    if (s->highFever || v->temperatureC >= 38.5f) fprintf(fp, "* Fever: give sips of water; tepid sponging.\n");
    if (s->fractureOrMajorTrauma) fprintf(fp, "* Immobilize limb; avoid unnecessary movement.\n");
    fprintf(fp, "* Keep patient warm and calm.\n");
    (void)p;
}

void printReceipt(const Patient *p, const Vitals *v, const Symptoms *s, bool emergency, const char* doctor) {
    // Generate unique filename with timestamp
    char filename[64];
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    snprintf(filename, sizeof(filename), "patient_receipt_%02d%02d%04d_%02d%02d.txt",
             t->tm_mday, t->tm_mon + 1, t->tm_year + 1900, t->tm_hour, t->tm_min);

    FILE *fp = fopen(filename, "w");
    if (!fp) {
        fprintf(stderr, "Error: Could not create receipt file.\n");
        return;
    }

    fprintf(fp, "================= HOSPITAL INITIAL SCREENING RECEIPT =================\n");
    fprintf(fp, "Patient Name   : %s\n", p->name);
    fprintf(fp, "Age / Gender   : %d / %s\n", p->age, p->gender);
    fprintf(fp, "Contact        : %s\n", p->contact);
    fprintf(fp, "Arrival Time   : %s\n", p->arrivalTime);
    fprintf(fp, "\nVitals -> Temp: %.1f C | HR: %d bpm | BP: %d/%d mmHg | SpO2: %d%%\n",
            v->temperatureC, v->heartRate, v->systolicBP, v->diastolicBP, v->spo2);
    fprintf(fp, "\nClassification : %s\n", emergency ? "EMERGENCY (Immediate attention)" : "NORMAL (Non-emergency)");
    fprintf(fp, "Allocated Dept : %s\n", doctor);
    printPrecautions(fp, p, v, s, emergency);
    fprintf(fp, "\n*** Please show this receipt at the designated desk ***\n");
    fprintf(fp, "=======================================================================\n");

    fclose(fp);
    printf("\nReceipt generated: %s\n", filename);
}

int main(void) {
    Patient p;
    Vitals v;
    Symptoms s;

    inputPatient(&p);
    inputVitals(&v);
    inputSymptoms(&s);

    bool emergency = isEmergency(&p, &v, &s);
    const char* doctor = allocateDoctor(&p, &v, &s, emergency);

    printf("\n--- Screening Summary ---\n");
    printf("Name        : %s\n", p.name);
    printf("Classification: %s\n", emergency ? "EMERGENCY" : "NORMAL");
    printf("Assigned to : %s\n", doctor);

    printReceipt(&p, &v, &s, emergency, doctor);

    printf("\nProceed to: %s Desk\n", emergency ? "Emergency Triage" : "Registration");
    return 0;
}
