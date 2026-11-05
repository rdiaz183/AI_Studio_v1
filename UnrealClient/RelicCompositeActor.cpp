#include "RelicCompositeActor.h"

ARelicCompositeActor::ARelicCompositeActor()
{
    PrimaryActorTick.bCanEverTick = false;

    // 1. Obelisk Base Setup with Chaos Physics
    ObeliskBase = CreateDefaultSubobject<UStaticMeshComponent>(TEXT("ObeliskBase"));
    RootComponent = ObeliskBase;

    ObeliskBase->SetSimulatePhysics(true);
    ObeliskBase->SetEnableGravity(false);
    ObeliskBase->SetCollisionProfileName(UCollisionProfile::PhysicsActor_ProfileName);
    ObeliskBase->SetMassOverrideInKg(NAME_None, 1850.0f, true);
    ObeliskBase->SetLinearDamping(0.75f);
    ObeliskBase->SetAngularDamping(0.50f);

    // 2. Icosahedron Apex Attachment
    IcosahedronApex = CreateDefaultSubobject<UProceduralMeshComponent>(TEXT("IcosahedronApex"));
    IcosahedronApex->SetupAttachment(RootComponent);
    IcosahedronApex->SetRelativeLocation(FVector(0.0f, 0.0f, 280.0f));
}

void ARelicCompositeActor::BeginPlay()
{
    Super::BeginPlay();

    BuildProceduralIcosahedron();

    // 10-Minute Gameplay Timer (600.0s)
    GetWorldTimerManager().SetTimer(
        TenMinuteTimerHandle,
        this,
        &ARelicCompositeActor::TriggerTenMinuteCutscene,
        600.0f,
        false
    );
}

void ARelicCompositeActor::BuildProceduralIcosahedron()
{
    TArray<FVector> Vertices;
    TArray<int32> Triangles;

    const float Phi = (1.0f + FMath::Sqrt(5.0f)) * 0.5f;
    const float R = 60.0f;

    Vertices.Add(FVector(-1.0f,  Phi, 0.0f) * R);
    Vertices.Add(FVector( 1.0f,  Phi, 0.0f) * R);
    Vertices.Add(FVector(-1.0f, -Phi, 0.0f) * R);
    Vertices.Add(FVector( 1.0f, -Phi, 0.0f) * R);
    Vertices.Add(FVector(0.0f, -1.0f,  Phi) * R);
    Vertices.Add(FVector(0.0f,  1.0f,  Phi) * R);
    Vertices.Add(FVector(0.0f, -1.0f, -Phi) * R);
    Vertices.Add(FVector(0.0f,  1.0f, -Phi) * R);
    Vertices.Add(FVector( Phi, 0.0f, -1.0f) * R);
    Vertices.Add(FVector( Phi, 0.0f,  1.0f) * R);
    Vertices.Add(FVector(-Phi, 0.0f, -1.0f) * R);
    Vertices.Add(FVector(-Phi, 0.0f,  1.0f) * R);

    Triangles.Append({0, 11, 5,  0, 5, 1,  0, 1, 7,  0, 7, 10,  0, 10, 11});
    Triangles.Append({1, 5, 9,   5, 11, 4, 11, 10, 2, 10, 7, 6,  7, 1, 8});
    Triangles.Append({3, 9, 4,   3, 4, 2,  3, 2, 6,  3, 6, 8,   3, 8, 9});
    Triangles.Append({4, 9, 5,   2, 4, 11, 6, 2, 10, 8, 6, 7,   9, 8, 1});

    IcosahedronApex->CreateMeshSection_LinearColor(
        0, Vertices, Triangles, TArray<FVector>(), TArray<FVector2D>(),
        TArray<FLinearColor>(), TArray<FProcMeshTangent>(), false
    );
}

void ARelicCompositeActor::TriggerTenMinuteCutscene()
{
    if (!RelicAwakeningSequence) return;

    FMovieSceneSequencePlaybackSettings Settings;
    Settings.bAutoPlay = true;
    Settings.bDisableMovementInput = true;
    Settings.bDisableLookAtInput = true;

    ALevelSequenceActor* OutActor = nullptr;
    ULevelSequencePlayer* Player = ULevelSequencePlayer::CreateLevelSequencePlayer(
        GetWorld(), RelicAwakeningSequence, Settings, OutActor
    );

    if (Player)
    {
        Player->Play();
        GEngine->AddOnScreenDebugMessage(-1, 10.0f, FColor::Cyan, TEXT(">> 10-MINUTE CINEMATIC TRIGGERED: Relic Awakening <<"));
    }
}
