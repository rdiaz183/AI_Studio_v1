#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "Components/StaticMeshComponent.h"
#include "ProceduralMeshComponent.h"
#include "LevelSequenceActor.h"
#include "LevelSequencePlayer.h"
#include "RelicCompositeActor.generated.h"

UCLASS()
class RELICPROTOTYPE_API ARelicCompositeActor : public AActor
{
    GENERATED_BODY()

public:
    ARelicCompositeActor();

protected:
    virtual void BeginPlay() override;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Relic|Components")
    TObjectPtr<UStaticMeshComponent> ObeliskBase;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Relic|Components")
    TObjectPtr<UProceduralMeshComponent> IcosahedronApex;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Relic|Cinematic")
    TObjectPtr<ULevelSequence> RelicAwakeningSequence;

    FTimerHandle TenMinuteTimerHandle;

    void BuildProceduralIcosahedron();
    void TriggerTenMinuteCutscene();
};
