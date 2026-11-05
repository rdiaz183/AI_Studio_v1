using UnrealBuildTool;

public class RelicPrototype : ModuleRules
{
    public RelicPrototype(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        CppStandard = CppStandardVersion.Cpp20;

        PublicDependencyModuleNames.AddRange(new string[] {
            "Core",
            "CoreUObject",
            "Engine",
            "InputCore",
            "Networking",
            "Sockets",
            "ProceduralMeshComponent",
            "LevelSequence",
            "MovieScene",
            "Chaos",
            "PhysicsCore"
        });
    }
}
